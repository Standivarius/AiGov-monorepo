from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel, Field, model_validator


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


class AuditProcedureStep(BaseModel):
    order: int = Field(ge=1)
    instruction: str = Field(min_length=3)


class EvidenceRequirement(BaseModel):
    id: str = Field(min_length=2)
    description: str = Field(min_length=3)
    required: bool = True
    acceptable_artifacts: list[str] = Field(default_factory=list)


class FindingCriterion(BaseModel):
    id: str = Field(min_length=2)
    if_condition: str = Field(min_length=3)
    then_outcome: Literal["FAIL", "PASS", "UNDECIDED"] = "FAIL"
    judge_instruction: str = Field(min_length=3)


class GdprArticleMapping(BaseModel):
    article: str = Field(description="GDPR article reference, e.g. 28, 32(1), 5(1)(a)")
    article_path: str | None = Field(
        default=None,
        description="Repo-relative path to local GDPR article file if found",
    )
    mapping_type: Literal["explicit", "context_inherited", "unmapped"] = "explicit"
    source_snippet: str | None = None


class MasterAuditRule(BaseModel):
    id: str = Field(min_length=2)
    title: str = ""
    requirement: str = Field(min_length=3)
    audit_procedure: list[AuditProcedureStep] = Field(default_factory=list)
    evidence_requirements: list[EvidenceRequirement] = Field(default_factory=list)
    finding_criteria: list[FindingCriterion] = Field(default_factory=list)
    gdpr_article_mappings: list[GdprArticleMapping] = Field(default_factory=list)
    source_pages: list[int] = Field(default_factory=list)
    source_section: str | None = None
    validation_issues: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def _normalize_pages(self) -> "MasterAuditRule":
        self.source_pages = sorted({p for p in self.source_pages if p > 0})
        return self


class MasterAuditCatalog(BaseModel):
    source_document: str
    generated_at_utc: str = Field(default_factory=utc_now_iso)
    parser: str
    extraction_mode: Literal["deterministic-self-correcting"] = "deterministic-self-correcting"
    rules: list[MasterAuditRule] = Field(default_factory=list)
    stats: dict[str, Any] = Field(default_factory=dict)

    def get_rule(self, rule_id: str | None = None) -> MasterAuditRule:
        if not self.rules:
            raise ValueError("No rules found in catalog.")
        if rule_id is None:
            return self.rules[0]
        for rule in self.rules:
            if rule.id == rule_id:
                return rule
        raise KeyError(f"Rule id not found: {rule_id}")

    @classmethod
    def from_file(cls, path: Path) -> "MasterAuditCatalog":
        if not path.exists():
            raise FileNotFoundError(f"Catalog not found: {path}")
        suffix = path.suffix.lower()
        raw = path.read_text(encoding="utf-8")
        if suffix in {".yaml", ".yml"}:
            return cls.model_validate(yaml.safe_load(raw))
        return cls.model_validate(json.loads(raw))

    def to_json_file(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(self.model_dump(mode="json"), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def to_yaml_file(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            yaml.safe_dump(self.model_dump(mode="json"), sort_keys=False, allow_unicode=True),
            encoding="utf-8",
        )


class JudgeVerdict(BaseModel):
    audited_topic: str
    gdpr_article: str
    compliance_score_0_to_100: int = Field(ge=0, le=100)
    evidence_found: str
    missing_controls: str
    severity: Literal["Low", "Medium", "High"]
    canonical_verdict: Literal["INFRINGEMENT", "COMPLIANT", "UNDECIDED"]
