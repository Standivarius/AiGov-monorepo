from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--file",
        default=str(Path(__file__).resolve().parent / "data" / "master_audit_rules.json"),
    )
    args = parser.parse_args()
    path = Path(args.file).resolve()
    print(f"file={path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    rules = data.get("rules", [])

    print(f"total_rules={len(rules)}")
    ids = [r.get("id", "") for r in rules]
    print(f"unique_ids={len(set(ids))}")
    dupes = Counter(ids).most_common(15)
    print("top_duplicates=")
    for item, count in dupes:
        if count > 1:
            print(f"  {item}: {count}")

    print("\nfirst_15_rules:")
    for r in rules[:15]:
        rid = r.get("id", "")
        title = (r.get("title") or "")[:90]
        req = (r.get("requirement") or "")[:140]
        pages = r.get("source_pages", [])
        issues = len(r.get("validation_issues", []))
        mappings = len(r.get("gdpr_article_mappings", []))
        print(
            f"- id={rid} pages={pages[:5]} mappings={mappings} issues={issues}\n"
            f"  title={title}\n"
            f"  requirement={req}"
        )

    with_map = sum(1 for r in rules if r.get("gdpr_article_mappings"))
    with_issues = sum(1 for r in rules if r.get("validation_issues"))
    print("\ncoverage:")
    print(f"  mapped_rules={with_map}")
    print(f"  issue_rules={with_issues}")


if __name__ == "__main__":
    main()
