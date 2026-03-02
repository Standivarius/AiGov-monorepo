from __future__ import annotations

import re
from pathlib import Path

from pypdf import PdfReader


def normalize_line(text: str) -> str:
    text = text.replace("\u00a0", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def main() -> None:
    pdf = Path(__file__).resolve().parent / "docs_auditor_manual" / "edpb_d2_audit_methodology.pdf"
    reader = PdfReader(str(pdf))
    pattern = re.compile(r"\b([A-Z][A-Z_]{1,40})\s+(\d+(?:\.[a-z])?)\s+(basic|advanced|optional)\b")
    hits = []
    for i, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        for raw in text.splitlines():
            line = normalize_line(raw)
            if not line:
                continue
            m = pattern.search(line)
            if m:
                hits.append((i, line))
    print(f"hits={len(hits)}")
    for page, line in hits[:80]:
        print(f"[p{page}] {line}")

    try:
        import fitz  # type: ignore

        doc = fitz.open(pdf)
        fitz_hits = []
        for i, page in enumerate(doc, start=1):
            text = page.get_text("text")
            for raw in text.splitlines():
                line = normalize_line(raw)
                if not line:
                    continue
                m = pattern.search(line)
                if m:
                    fitz_hits.append((i, line))
        print(f"\nfitz_hits={len(fitz_hits)}")
        for page, line in fitz_hits[:80]:
            print(f"[fitz p{page}] {line}")
    except Exception as exc:
        print(f"\nfitz_unavailable={exc}")


if __name__ == "__main__":
    main()
