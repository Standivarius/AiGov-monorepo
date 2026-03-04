from __future__ import annotations

import argparse
import csv
import json
import re
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _article_num_from_ref(text: str) -> str | None:
    match = re.search(r"(\d{1,2})", text or "")
    if not match:
        return None
    return str(int(match.group(1)))


def _load_gpt_pack(pack_input: Path) -> tuple[dict[str, Any], list[dict[str, str]]]:
    if not pack_input.exists():
        raise FileNotFoundError(f"Pack input not found: {pack_input}")

    if pack_input.suffix.lower() == ".zip":
        with zipfile.ZipFile(pack_input, "r") as zf:
            yaml_name = "gdpr_audit_pack.yaml"
            csv_name = "sources_register.csv"
            with zf.open(yaml_name, "r") as f:
                pack = yaml.safe_load(f.read().decode("utf-8"))
            source_rows: list[dict[str, str]] = []
            with zf.open(csv_name, "r") as f:
                decoded = f.read().decode("utf-8").splitlines()
                for row in csv.DictReader(decoded):
                    source_rows.append({k: str(v) for k, v in row.items()})
            return pack, source_rows

    pack = yaml.safe_load(pack_input.read_text(encoding="utf-8"))
    return pack, []


def _flatten_source_rows(pack: dict[str, Any], source_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    if source_rows:
        return source_rows

    dedup: dict[tuple[str, str], dict[str, str]] = {}
    rules = ((pack.get("pack") or {}).get("rules") or [])
    for rule in rules:
        for ref in (rule.get("source_refs") or []):
            key = (str(ref.get("title", "")).strip(), str(ref.get("locator", "")).strip())
            if key not in dedup:
                dedup[key] = {
                    "source_type": str(ref.get("source_type", "")),
                    "title": str(ref.get("title", "")),
                    "url": str(ref.get("url", "")),
                    "locator": str(ref.get("locator", "")),
                }
    return list(dedup.values())


def _validate_pack(pack: dict[str, Any], source_rows: list[dict[str, str]]) -> dict[str, Any]:
    payload = pack.get("pack") or {}
    rules = payload.get("rules") or []
    required = [
        "rule_id",
        "article",
        "paragraph",
        "canonical_obligation_text",
        "trigger_condition",
        "minimum_evidence_expectation",
        "deterministic_failure_test",
        "source_refs",
        "duty_holder",
    ]

    missing_fields: list[dict[str, Any]] = []
    seen: set[str] = set()
    duplicate_ids: list[str] = []
    excluded_non_testable: list[str] = []
    draft_marked: list[str] = []

    for rule in rules:
        rule_id = str(rule.get("rule_id", "")).strip()
        if not rule_id:
            continue
        if rule_id in seen:
            duplicate_ids.append(rule_id)
        seen.add(rule_id)

        miss = [k for k in required if k not in rule or rule.get(k) in (None, "", [])]
        if miss:
            missing_fields.append({"rule_id": rule_id, "missing": miss})

        if str(rule.get("duty_holder", "")).strip().lower() == "n/a":
            excluded_non_testable.append(rule_id)

        refs = rule.get("source_refs") or []
        ref_text = " ".join([json.dumps(r, ensure_ascii=False) for r in refs]).lower()
        if any(flag in ref_text for flag in ["draft", "public consultation", "consultation"]):
            draft_marked.append(rule_id)

    raw_count = len(rules)
    testable_count = len([r for r in rules if str(r.get("duty_holder", "")).strip().lower() != "n/a"])

    return {
        "pack_id": payload.get("id"),
        "pack_name": payload.get("name"),
        "pack_version": payload.get("version"),
        "generated_at": payload.get("generated_at"),
        "raw_rule_count": raw_count,
        "testable_rule_count": testable_count,
        "required_fields": required,
        "missing_fields_count": len(missing_fields),
        "missing_fields": missing_fields,
        "duplicate_rule_id_count": len(duplicate_ids),
        "duplicate_rule_ids": sorted(set(duplicate_ids)),
        "excluded_non_testable_count": len(excluded_non_testable),
        "excluded_non_testable_rule_ids": sorted(excluded_non_testable),
        "draft_marker_count": len(draft_marked),
        "draft_marker_rule_ids": sorted(draft_marked),
        "source_register_count": len(source_rows),
    }


def _to_d2_shape(rule: dict[str, Any]) -> dict[str, Any]:
    rule_id = str(rule.get("rule_id", "")).strip()
    article = str(rule.get("article", "")).strip()
    paragraph = str(rule.get("paragraph", "")).strip()

    title = f"GDPR Art {article}({paragraph})" if paragraph else f"GDPR Art {article}"
    requirement = str(rule.get("canonical_obligation_text", "")).strip()
    trigger = str(rule.get("trigger_condition", "")).strip()
    failure = str(rule.get("deterministic_failure_test", "")).strip()
    evidence = rule.get("minimum_evidence_expectation", {}) or {}
    documentary = evidence.get("documentary", []) or []
    technical = evidence.get("technical", []) or []
    procedural = evidence.get("procedural", []) or []

    audit_procedure = [
        {"order": 1, "instruction": f"Confirm trigger scope: {trigger}"},
        {"order": 2, "instruction": "Collect documentary, technical, and procedural evidence listed for this rule."},
        {"order": 3, "instruction": "Apply deterministic failure test exactly as written."},
    ]

    evidence_requirements: list[dict[str, str]] = []
    for item in documentary:
        evidence_requirements.append({"category": "documentary", "expectation": str(item)})
    for item in technical:
        evidence_requirements.append({"category": "technical", "expectation": str(item)})
    for item in procedural:
        evidence_requirements.append({"category": "procedural", "expectation": str(item)})

    article_mappings: list[dict[str, str]] = []
    if article:
        article_mappings.append(
            {
                "article": article,
                "article_path": "",
                "mapping_type": "legal_primary",
                "source_snippet": f"Primary mapping from rule {rule_id}.",
            }
        )
    for rel in rule.get("related_articles", []) or []:
        rel_num = _article_num_from_ref(str(rel))
        if rel_num:
            article_mappings.append(
                {
                    "article": rel_num,
                    "article_path": "",
                    "mapping_type": "legal_related",
                    "source_snippet": str(rel),
                }
            )

    refs = rule.get("source_refs", []) or []
    issues: list[str] = []
    ref_text = " ".join([json.dumps(r, ensure_ascii=False) for r in refs]).lower()
    if any(flag in ref_text for flag in ["draft", "public consultation", "consultation"]):
        issues.append("Contains non-final guidance marker in source refs.")

    return {
        "id": rule_id,
        "title": title,
        "requirement": requirement,
        "audit_procedure": audit_procedure,
        "evidence_requirements": evidence_requirements,
        "finding_criteria": [
            {
                "id": "FC-01",
                "if_condition": failure,
                "then_outcome": "FAIL",
                "judge_instruction": "Return FAIL when condition is met; otherwise continue evaluation.",
            }
        ],
        "gdpr_article_mappings": article_mappings,
        "source_pages": [],
        "source_section": rule_id,
        "validation_issues": issues,
        "source_refs": refs,
        "confidence": float(rule.get("confidence", 0.0) or 0.0),
        "_provenance": {
            "source_pack": "gdpr_audit_pack",
            "source_rule_id": rule_id,
            "legal_basis_type": str(rule.get("legal_basis_type", "")),
            "obligation_kind": str(rule.get("obligation_kind", "")),
            "duty_holder": str(rule.get("duty_holder", "")),
        },
    }


def _article_signal_map() -> dict[str, list[str]]:
    return {
        "5": [
            "unlawful_processing",
            "inadequate_transparency",
            "purpose_limitation_breach",
            "data_minimization_breach",
            "accuracy_violation",
            "retention_violation",
            "inadequate_security",
        ],
        "6": ["unlawful_processing", "lack_of_consent"],
        "7": ["lack_of_consent"],
        "8": ["children_data_violation", "lack_of_consent"],
        "9": ["special_category_violation", "unlawful_processing"],
        "12": ["inadequate_transparency", "rights_violation"],
        "13": ["inadequate_transparency"],
        "14": ["inadequate_transparency"],
        "15": ["rights_violation"],
        "16": ["rights_violation", "accuracy_violation"],
        "17": ["rights_violation", "retention_violation"],
        "18": ["rights_violation"],
        "20": ["rights_violation"],
        "21": ["rights_violation"],
        "22": ["profiling_without_safeguards", "rights_violation"],
        "24": ["accountability_breach"],
        "25": ["data_minimization_breach", "accountability_breach"],
        "28": ["processor_contract_violation", "accountability_breach"],
        "30": ["accountability_breach"],
        "32": ["inadequate_security"],
        "33": ["breach_notification_failure"],
        "34": ["breach_notification_failure"],
        "35": ["missing_dpia"],
        "36": ["missing_dpia"],
        "37": ["inadequate_dpo"],
        "44": ["international_transfer_violation"],
        "45": ["international_transfer_violation"],
        "46": ["international_transfer_violation"],
        "47": ["international_transfer_violation"],
        "48": ["international_transfer_violation"],
        "49": ["international_transfer_violation"],
    }


def _keyword_signal_pairs() -> list[tuple[str, str]]:
    return [
        ("consent", "lack_of_consent"),
        ("transparen", "inadequate_transparency"),
        ("purpose", "purpose_limitation_breach"),
        ("minimis", "data_minimization_breach"),
        ("retention", "retention_violation"),
        ("security", "inadequate_security"),
        ("breach", "breach_notification_failure"),
        ("special categor", "special_category_violation"),
        ("child", "children_data_violation"),
        ("automated decision", "profiling_without_safeguards"),
        ("profil", "profiling_without_safeguards"),
        ("transfer", "international_transfer_violation"),
        ("processor", "processor_contract_violation"),
        ("dpia", "missing_dpia"),
        ("dpo", "inadequate_dpo"),
        ("accountab", "accountability_breach"),
        ("accuracy", "accuracy_violation"),
        ("erase", "rights_violation"),
        ("access", "rights_violation"),
        ("object", "rights_violation"),
        ("portability", "rights_violation"),
    ]


def _build_crosswalk(
    adapted_rules: list[dict[str, Any]],
    allowed_signals: set[str],
) -> dict[str, Any]:
    by_article = _article_signal_map()
    keyword_pairs = _keyword_signal_pairs()
    rows: list[dict[str, Any]] = []

    for rule in adapted_rules:
        rid = str(rule.get("id", ""))
        mappings = rule.get("gdpr_article_mappings", []) or []
        articles = []
        for m in mappings:
            art = _article_num_from_ref(str(m.get("article", "")))
            if art:
                articles.append(art)

        signals: set[str] = set()
        reasons: list[str] = []

        for art in articles:
            for sig in by_article.get(art, []):
                if sig in allowed_signals:
                    signals.add(sig)
                    reasons.append(f"article:{art}->{sig}")

        hay = f"{rule.get('requirement','')} {json.dumps(rule.get('finding_criteria',[]), ensure_ascii=False)}".lower()
        for key, sig in keyword_pairs:
            if key in hay and sig in allowed_signals:
                signals.add(sig)
                reasons.append(f"keyword:{key}->{sig}")

        if not signals:
            status = "manual_required"
        else:
            article_hits = [r for r in reasons if r.startswith("article:")]
            status = "direct" if article_hits else "derived"

        rows.append(
            {
                "rule_id": rid,
                "article_numbers": sorted(set(articles)),
                "signal_ids": sorted(signals),
                "mapping_status": status,
                "reasons": sorted(set(reasons)),
            }
        )

    counts = {"direct": 0, "derived": 0, "manual_required": 0}
    for row in rows:
        counts[row["mapping_status"]] += 1

    return {
        "generated_at_utc": _utc_now(),
        "total_rules": len(rows),
        "status_counts": counts,
        "rows": rows,
    }


def _load_signals(signal_contract_path: Path) -> set[str]:
    payload = json.loads(signal_contract_path.read_text(encoding="utf-8"))
    return set(payload.get("signal_ids", []))


def _extract_case_articles(case_payload: dict[str, Any]) -> set[str]:
    expected = case_payload.get("expected_outcome", {})
    refs = expected.get("gdpr_citations") or expected.get("gdpr_refs") or []
    out: set[str] = set()
    for ref in refs:
        art = _article_num_from_ref(str(ref))
        if art:
            out.add(art)
    return out


def _extract_case_signals(case_payload: dict[str, Any]) -> set[str]:
    expected = case_payload.get("expected_outcome", {})
    req = expected.get("required_signals", []) or []
    extra = expected.get("allowed_extra_signals", []) or []
    return set([str(x) for x in req + extra])


def _load_d2_mapping(mapping_path: Path) -> dict[str, list[str]]:
    if not mapping_path.exists():
        return {}
    raw = json.loads(mapping_path.read_text(encoding="utf-8"))
    out: dict[str, list[str]] = {}
    for case_id, val in raw.items():
        if isinstance(val, list):
            out[case_id] = [str(x) for x in val]
    return out


def _build_case_mapping(
    case_dir: Path,
    adapted_rules: list[dict[str, Any]],
    crosswalk: dict[str, Any],
    d2_mapping: dict[str, list[str]],
    cap_per_case: int,
) -> dict[str, Any]:
    rule_by_id = {str(r.get("id", "")): r for r in adapted_rules}
    xw_by_id = {str(r["rule_id"]): r for r in crosswalk.get("rows", [])}

    cases: dict[str, Any] = {}
    for case_path in sorted(case_dir.glob("*.json")):
        case = json.loads(case_path.read_text(encoding="utf-8"))
        case_id = str(case.get("scenario_id") or case_path.stem)
        articles = _extract_case_articles(case)
        expected_signals = _extract_case_signals(case)

        candidates: list[dict[str, Any]] = []
        for rid, rule in rule_by_id.items():
            xw = xw_by_id.get(rid, {})
            rule_articles = set(xw.get("article_numbers", []))
            if not articles or articles.intersection(rule_articles):
                signals = set(xw.get("signal_ids", []))
                signal_overlap = len(signals.intersection(expected_signals)) if expected_signals else 0
                status = xw.get("mapping_status", "manual_required")
                status_weight = {"direct": 3, "derived": 2, "manual_required": 1}.get(status, 1)
                confidence = float(rule.get("confidence", 0.0) or 0.0)
                candidates.append(
                    {
                        "rule_id": rid,
                        "signal_overlap": signal_overlap,
                        "status_weight": status_weight,
                        "confidence": confidence,
                    }
                )

        candidates.sort(
            key=lambda x: (x["signal_overlap"], x["status_weight"], x["confidence"], x["rule_id"]),
            reverse=True,
        )
        legal_rule_ids = [c["rule_id"] for c in candidates[:cap_per_case]]

        # Fallback for difficult cases: if still empty and case is not compliant control.
        expected_verdict = str((case.get("expected_outcome", {}) or {}).get("verdict", "")).upper()
        if not legal_rule_ids and expected_verdict != "COMPLIANT":
            broad = sorted(rule_by_id.values(), key=lambda r: float(r.get("confidence", 0.0) or 0.0), reverse=True)
            legal_rule_ids = [str(r.get("id", "")) for r in broad[: min(5, cap_per_case)] if str(r.get("id", ""))]

        procedural_rule_ids = list(d2_mapping.get(case_id, []))[: min(5, cap_per_case)]
        combined = list(dict.fromkeys(legal_rule_ids + procedural_rule_ids))

        cases[case_id] = {
            "legal_rule_ids": legal_rule_ids,
            "procedural_rule_ids": procedural_rule_ids,
            "combined_rule_ids": combined,
            "articles": sorted(articles),
            "expected_signals": sorted(expected_signals),
        }

    return {
        "generated_at_utc": _utc_now(),
        "cap_per_case": cap_per_case,
        "cases": cases,
    }


def _write_yaml(path: Path, payload: Any) -> None:
    path.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=True), encoding="utf-8")


def _write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def _write_md(path: Path, validation: dict[str, Any], crosswalk: dict[str, Any], mapping: dict[str, Any]) -> None:
    status = crosswalk.get("status_counts", {})
    cases = mapping.get("cases", {})
    non_empty_legal = sum(1 for c in cases.values() if c.get("legal_rule_ids"))
    non_empty_combined = sum(1 for c in cases.values() if c.get("combined_rule_ids"))

    lines = [
        "# GDPR Rules Replacement - Phase 1-4 Report (v1)",
        "",
        f"- Generated at (UTC): `{_utc_now()}`",
        f"- Raw rules: `{validation.get('raw_rule_count')}`",
        f"- Testable rules: `{validation.get('testable_rule_count')}`",
        f"- Excluded non-testable (`duty_holder=n/a`): `{validation.get('excluded_non_testable_count')}`",
        f"- Missing-field rows: `{validation.get('missing_fields_count')}`",
        f"- Duplicate IDs: `{validation.get('duplicate_rule_id_count')}`",
        f"- Draft-marked rules: `{validation.get('draft_marker_count')}`",
        "",
        "## Crosswalk status",
        f"- direct: `{status.get('direct', 0)}`",
        f"- derived: `{status.get('derived', 0)}`",
        f"- manual_required: `{status.get('manual_required', 0)}`",
        "",
        "## Case mapping coverage (12 calibration set)",
        f"- Cases with legal mappings: `{non_empty_legal}/{len(cases)}`",
        f"- Cases with combined mappings (legal+procedural): `{non_empty_combined}/{len(cases)}`",
        "",
        "## Notes",
        "- Dual-pack strategy applied: legal-first GPT pack, procedural fallback from D2 mapping.",
        "- Outputs are additive (`*_gdpr_v1`) and do not overwrite old D2 files.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build GDPR legal pack adapter and mappings (Phase 1-4).")
    parser.add_argument(
        "--pack-input",
        default=r"C:\Users\User\OneDrive - DMR Ergonomics\gdpr_audit_pack.zip",
        help="Path to gdpr_audit_pack.zip or gdpr_audit_pack.yaml",
    )
    parser.add_argument(
        "--output-dir",
        default=str(Path(__file__).resolve().parent / "data"),
        help="Output directory for generated artifacts.",
    )
    parser.add_argument(
        "--signals-path",
        default=str(Path(__file__).resolve().parents[3] / "packages" / "pe" / "aigov_eval" / "taxonomy" / "contracts" / "signals.json"),
        help="Path to AiGov signals taxonomy contract.",
    )
    parser.add_argument(
        "--cases-dir",
        default=str(Path(__file__).resolve().parents[3] / "packages" / "pe" / "cases" / "calibration"),
        help="Path to calibration cases directory.",
    )
    parser.add_argument(
        "--d2-mapping-path",
        default=str(Path(__file__).resolve().parent / "data" / "calibration_to_edpb_rules.json"),
        help="Path to existing D2 case mapping for procedural fallback.",
    )
    parser.add_argument("--cap-per-case", type=int, default=12, help="Max legal rules per case.")
    args = parser.parse_args()

    pack_input = Path(args.pack_input)
    output_dir = Path(args.output_dir)
    signals_path = Path(args.signals_path)
    cases_dir = Path(args.cases_dir)
    d2_mapping_path = Path(args.d2_mapping_path)

    output_dir.mkdir(parents=True, exist_ok=True)

    pack, source_rows = _load_gpt_pack(pack_input)
    source_rows = _flatten_source_rows(pack, source_rows)
    validation = _validate_pack(pack, source_rows)
    pack_rules = ((pack.get("pack") or {}).get("rules") or [])
    testable = [r for r in pack_rules if str(r.get("duty_holder", "")).strip().lower() != "n/a"]
    adapted_rules = [_to_d2_shape(r) for r in testable]

    adapted_payload = {
        "version": "gdpr_v1",
        "generated_at_utc": _utc_now(),
        "source_pack": (pack.get("pack") or {}).get("id"),
        "rules": adapted_rules,
    }

    allowed_signals = _load_signals(signals_path)
    crosswalk = _build_crosswalk(adapted_rules, allowed_signals)
    d2_mapping = _load_d2_mapping(d2_mapping_path)
    case_mapping = _build_case_mapping(
        case_dir=cases_dir,
        adapted_rules=adapted_rules,
        crosswalk=crosswalk,
        d2_mapping=d2_mapping,
        cap_per_case=args.cap_per_case,
    )
    flat_mapping = {
        case_id: payload.get("combined_rule_ids", [])
        for case_id, payload in case_mapping.get("cases", {}).items()
    }

    _write_yaml(output_dir / "master_audit_rules_gdpr_v1.yaml", adapted_payload)
    _write_json(output_dir / "master_audit_rules_gdpr_v1.json", adapted_payload)
    _write_json(output_dir / "gdpr_pack_validation_v1.json", validation)
    _write_json(output_dir / "gdpr_source_register_v1.json", source_rows)
    _write_json(output_dir / "gdpr_rule_signal_crosswalk_v1.json", crosswalk)
    _write_json(output_dir / "calibration_to_gdpr_rules_v1.json", case_mapping)
    _write_json(output_dir / "calibration_to_gdpr_rules_v1_flat.json", flat_mapping)
    _write_md(output_dir / "gdpr_rules_replacement_phase1_4_report_v1.md", validation, crosswalk, case_mapping)

    print(f"[ok] adapted rules: {len(adapted_rules)}")
    print(f"[ok] validation report: {output_dir / 'gdpr_pack_validation_v1.json'}")
    print(f"[ok] crosswalk: {output_dir / 'gdpr_rule_signal_crosswalk_v1.json'}")
    print(f"[ok] mapping: {output_dir / 'calibration_to_gdpr_rules_v1.json'}")


if __name__ == "__main__":
    main()
