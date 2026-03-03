from __future__ import annotations

import json
from pathlib import Path


def main() -> None:
    path = Path(__file__).resolve().parent / "data" / "calibration_to_edpb_rules.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    print(f"file={path}")
    print(f"cases={len(data)}")
    for case_id in sorted(data.keys()):
        print(f"{case_id}: {len(data[case_id])} rules")


if __name__ == "__main__":
    main()

