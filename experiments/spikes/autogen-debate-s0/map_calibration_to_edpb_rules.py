from __future__ import annotations

import json
import re
from pathlib import Path

import yaml


def normalize_article_number(text: str) -> str | None:
    match = re.search(r"(\d{1,2})", text or "")
    if not match:
        return None
    return str(int(match.group(1)))


def load_case_articles(case_path: Path) -> tuple[str, set[str]]:
    data = json.loads(case_path.read_text(encoding="utf-8"))
    case_id = data.get("scenario_id") or case_path.stem
    expected = data.get("expected_outcome", {})
    citations = expected.get("gdpr_citations") or expected.get("gdpr_refs") or []
    articles: set[str] = set()
    for citation in citations:
        article = normalize_article_number(str(citation))
        if article:
            articles.add(article)
    return case_id, articles


def load_rule_articles(rules_yaml_path: Path) -> dict[str, set[str]]:
    payload = yaml.safe_load(rules_yaml_path.read_text(encoding="utf-8")) or {}
    rules = payload.get("rules", [])
    mapping: dict[str, set[str]] = {}
    for rule in rules:
        rule_id = str(rule.get("id", "")).strip()
        if not rule_id:
            continue
        articles: set[str] = set()
        for item in rule.get("gdpr_article_mappings", []) or []:
            article = normalize_article_number(str(item.get("article", "")))
            if article:
                articles.add(article)
        if articles:
            mapping[rule_id] = articles
    return mapping


def build_mapping(cases_dir: Path, rules_yaml_path: Path) -> dict[str, list[str]]:
    rule_articles = load_rule_articles(rules_yaml_path)
    out: dict[str, list[str]] = {}

    for case_path in sorted(cases_dir.glob("*.json")):
        case_id, case_articles = load_case_articles(case_path)
        relevant_rule_ids: list[str] = []
        if case_articles:
            for rule_id, articles in rule_articles.items():
                if case_articles.intersection(articles):
                    relevant_rule_ids.append(rule_id)
        out[case_id] = sorted(relevant_rule_ids)
    return out


def main() -> None:
    spike_dir = Path(__file__).resolve().parent
    repo_root = spike_dir.parents[2]
    cases_dir = repo_root / "packages" / "pe" / "cases" / "calibration"
    rules_yaml_path = spike_dir / "data" / "master_audit_rules.yaml"
    out_path = spike_dir / "data" / "calibration_to_edpb_rules.json"

    if not cases_dir.exists():
        raise FileNotFoundError(f"Calibration cases directory not found: {cases_dir}")
    if not rules_yaml_path.exists():
        raise FileNotFoundError(f"Rules file not found: {rules_yaml_path}")

    mapping = build_mapping(cases_dir=cases_dir, rules_yaml_path=rules_yaml_path)
    out_path.write_text(json.dumps(mapping, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"[ok] cases mapped: {len(mapping)}")
    print(f"[ok] output: {out_path}")


if __name__ == "__main__":
    main()
