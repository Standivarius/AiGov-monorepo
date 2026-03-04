#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-safe", required=True)
    parser.add_argument("--cases", nargs="+", required=True)
    args = parser.parse_args()

    base = Path(__file__).resolve().parent / "work" / "case_diffs" / args.model_safe
    for case in args.cases:
        path = base / f"{case}_ab_result.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        g = payload["generic"]["score"]
        e = payload["enriched"]["score"]
        print(f"CASE: {case}")
        print(f"RULES: {payload.get('edpb_rule_ids', [])}")
        print(
            "GENERIC:",
            g["pred_verdict"],
            g["pred_signals"],
            g["pred_articles"],
            f"q={g['quality_score']:.3f}",
            f"rr={g['required_recall']:.3f}",
            f"sp={g['signal_precision_allowed']:.3f}",
            f"cr={g['citation_recall']:.3f}",
        )
        print(
            "ENRICHED:",
            e["pred_verdict"],
            e["pred_signals"],
            e["pred_articles"],
            f"q={e['quality_score']:.3f}",
            f"rr={e['required_recall']:.3f}",
            f"sp={e['signal_precision_allowed']:.3f}",
            f"cr={e['citation_recall']:.3f}",
        )
        preview = payload.get("contexts_used", {}).get("edpb_context_preview", "")
        preview = preview.replace("\n", " | ")
        print(f"CTX_PREVIEW: {preview[:800]}")
        print("---")


if __name__ == "__main__":
    main()
