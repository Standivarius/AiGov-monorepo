#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CAL_DIR = ROOT / "packages" / "pe" / "cases" / "calibration"
MASTER_PATH = ROOT / "experiments" / "spikes" / "autogen-debate-s0" / "data" / "master_audit_rules.json"
MAP_PATH = ROOT / "experiments" / "spikes" / "autogen-debate-s0" / "data" / "calibration_to_edpb_rules.json"

CASES = [
    "cal_003_data_minimization",
    "cal_008_excessive_retention",
    "cal_012_transparency_violation",
]


def article_nums_from_text(values: list[str]) -> set[str]:
    out: set[str] = set()
    for v in values:
        for m in re.findall(r"Art\.?\s*([0-9]+)", str(v), flags=re.IGNORECASE):
            out.add(m)
    return out


def article_nums_from_rule(rule: dict) -> set[str]:
    out: set[str] = set()
    for item in rule.get("gdpr_article_mappings", []) or []:
        a = str(item.get("article", "")).strip()
        if a.isdigit():
            out.add(a)
    return out


def main() -> None:
    master = json.loads(MASTER_PATH.read_text(encoding="utf-8"))
    mapped = json.loads(MAP_PATH.read_text(encoding="utf-8"))

    rule_records = []
    for r in master.get("rules", []):
        rule_records.append(
            {
                "id": r.get("id"),
                "source_section": r.get("source_section", ""),
                "requirement": str(r.get("requirement", "")),
                "articles": article_nums_from_rule(r),
            }
        )

    print(f"TOTAL_RULES={len(rule_records)}")
    for target_article in ("5", "13", "14"):
        count = sum(1 for r in rule_records if target_article in r["articles"])
        print(f"ARTICLE_{target_article}_RULES={count}")

    print("\n=== CASE CHECK ===")
    for case_id in CASES:
        fixture = json.loads((CAL_DIR / f"{case_id}.json").read_text(encoding="utf-8"))
        citations = fixture.get("expected_outcome", {}).get("gdpr_citations", [])
        cited_articles = article_nums_from_text(citations)
        direct = [r for r in rule_records if r["articles"] & cited_articles]

        print(f"\n[{case_id}]")
        print(f"mapped_rule_ids={mapped.get(case_id, [])}")
        print(f"gdpr_citations={citations}")
        print(f"cited_articles={sorted(cited_articles)}")
        print(f"direct_article_match_rules={len(direct)}")
        if direct:
            print("direct_match_sample=" + ", ".join([r["id"] for r in direct[:12]]))

    # semantic/near-match hints under different article refs
    keyword_sets = {
        "cal_003_data_minimization": ["minimi", "necessary", "adequate", "relevant", "limited"],
        "cal_008_excessive_retention": ["retain", "retention", "storage", "erase", "delete"],
        "cal_012_transparency_violation": ["privacy policy", "transparen", "inform", "third party", "disclos", "purpose"],
    }

    print("\n=== NEAR MATCHES (keyword heuristic) ===")
    for case_id, keywords in keyword_sets.items():
        hits: list[tuple[int, dict]] = []
        for r in rule_records:
            blob = f"{r['id']} {r['source_section']} {r['requirement']}".lower()
            score = sum(1 for kw in keywords if kw in blob)
            if score > 0:
                hits.append((score, r))
        hits.sort(key=lambda x: (-x[0], x[1]["id"]))
        print(f"\n[{case_id}] top_near_matches=")
        for score, r in hits[:10]:
            arts = ",".join(sorted(r["articles"])) if r["articles"] else "-"
            print(f"  score={score} id={r['id']} articles={arts} source={r['source_section']}")

    print("\n=== TARGETED CANDIDATE GROUPS ===")
    transparency_ids = []
    retention_ids = []
    minimization_ids = []
    for r in rule_records:
        rid = (r["id"] or "").upper()
        source = (r["source_section"] or "").upper()
        req = (r["requirement"] or "").lower()

        if rid.startswith("POLICY_1") or "privacy policy" in req or "transparent" in req:
            transparency_ids.append(r)
        if rid.startswith("ACC_DEL_") or rid.startswith("DATA_DEL_") or "delete" in req or "retention" in req:
            retention_ids.append(r)
        if "minimiz" in req or "adequate" in req or "necessary" in req or rid.startswith("APP_BEHAV_"):
            minimization_ids.append(r)

    def _print_group(name: str, rows: list[dict], limit: int = 20) -> None:
        print(f"\n{name} (count={len(rows)})")
        rows = sorted(rows, key=lambda x: x["id"] or "")
        for r in rows[:limit]:
            arts = ",".join(sorted(r["articles"])) if r["articles"] else "-"
            snippet = r["requirement"][:90].replace("\n", " ")
            print(f"  id={r['id']} articles={arts} source={r['source_section']} req={snippet}")

    _print_group("transparency_like", transparency_ids)
    _print_group("retention_like", retention_ids)
    _print_group("minimization_like", minimization_ids)


if __name__ == "__main__":
    main()
