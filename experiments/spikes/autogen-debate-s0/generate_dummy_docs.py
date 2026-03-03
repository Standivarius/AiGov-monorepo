from __future__ import annotations

from pathlib import Path


def main() -> None:
    base = Path(__file__).resolve().parent
    auditor_dir = base / "docs_auditor_manual"
    client_dir = base / "docs_client_evidence"
    auditor_dir.mkdir(parents=True, exist_ok=True)
    client_dir.mkdir(parents=True, exist_ok=True)

    auditor_doc = auditor_dir / "dummy_edpb_method_excerpt.txt"
    client_doc = client_dir / "dummy_client_architecture.txt"

    auditor_doc.write_text(
        (
            "LEG_BASIS_1\n"
            "Requirement: Controller must demonstrate lawful basis for each processing purpose.\n"
            "Verification steps:\n"
            "1. Inspect records of processing and privacy notice.\n"
            "2. Verify declared legal basis is specific and documented.\n"
            "Evidence needed:\n"
            "- Records of processing activities (RoPA)\n"
            "- Privacy notice excerpt\n"
            "- DPA / processor contract excerpts\n"
            "Finding criteria:\n"
            "- If legal basis is missing for any purpose, FAIL.\n"
            "- If records are incomplete, FAIL.\n"
            "Guidelines: Article 6, Article 28.\n"
        ),
        encoding="utf-8",
    )

    client_doc.write_text(
        (
            "System: Chat assistant for municipal citizen requests.\n"
            "Controls:\n"
            "- RoPA maintained quarterly.\n"
            "- DPA template used with subprocessors.\n"
            "- Privacy notice links legal basis per service category.\n"
            "Gaps:\n"
            "- No explicit subprocessor change notification log.\n"
        ),
        encoding="utf-8",
    )

    print(f"[ok] wrote {auditor_doc}")
    print(f"[ok] wrote {client_doc}")


if __name__ == "__main__":
    main()

