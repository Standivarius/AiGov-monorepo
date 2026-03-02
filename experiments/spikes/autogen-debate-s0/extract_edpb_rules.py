from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Iterable

import requests

from schemas import (
    AuditProcedureStep,
    EvidenceRequirement,
    FindingCriterion,
    GdprArticleMapping,
    MasterAuditCatalog,
    MasterAuditRule,
)

DEFAULT_EDPB_PDF_URL = (
    "https://www.edpb.europa.eu/system/files/2024-06/"
    "standardisedmessengeraudit_d2audit-methodology_edpb-spe-programme_en.pdf"
)

CASE_ID_RE = re.compile(r"^(TC[-_ ]?\d+|[A-Z]{2,}(?:_[A-Z]+)*_\d{1,3})\b")
CASE_START_RE = re.compile(
    r"\b([A-Z][A-Z_]*(?:\s+[A-Z][A-Z_]*){0,3})\s+(\d+(?:\.[a-z])?)\s+(basic|advanced|optional)\b"
)
ARTICLE_RE = re.compile(
    r"(?i)\b(?:gdpr\s*)?(?:article|art\.?)\s*(\d{1,2})(?:\s*\(([^)]+)\))?"
)

SECTION_ALIASES: dict[str, tuple[str, ...]] = {
    "requirement": (
        "requirement",
        "objective",
        "purpose",
        "what is being checked",
    ),
    "audit_procedure": (
        "verification steps",
        "audit procedure",
        "verification procedure",
        "test procedure",
    ),
    "evidence": (
        "evidence needed",
        "evidence required",
        "required evidence",
        "evidence to collect",
        "evidence",
    ),
    "finding": (
        "finding criteria",
        "failure criteria",
        "non-compliance criteria",
        "pass/fail criteria",
    ),
}


def parse_args() -> argparse.Namespace:
    root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser(
        description="Extract EDPB D2 test cases and map them to local GDPR article files."
    )
    parser.add_argument(
        "--pdf-url",
        default=DEFAULT_EDPB_PDF_URL,
        help="URL of the EDPB methodology PDF.",
    )
    parser.add_argument(
        "--pdf-path",
        default="docs_auditor_manual/edpb_d2_audit_methodology.pdf",
        help="Local PDF destination (downloaded if missing).",
    )
    parser.add_argument(
        "--repo-root",
        default=str(root),
        help="Repo root used to resolve local GDPR article files.",
    )
    parser.add_argument(
        "--output-json",
        default="data/master_audit_rules.json",
        help="Output JSON path.",
    )
    parser.add_argument(
        "--output-yaml",
        default="data/master_audit_rules.yaml",
        help="Output YAML path.",
    )
    parser.add_argument(
        "--max-cases",
        type=int,
        default=0,
        help="Optional cap for extracted cases (0 = all).",
    )
    return parser.parse_args()


def download_pdf(url: str, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if out_path.exists() and out_path.stat().st_size > 0:
        return
    response = requests.get(url, timeout=120)
    response.raise_for_status()
    out_path.write_bytes(response.content)


def extract_pages_text(pdf_path: Path) -> list[str]:
    # Preferred parser for this specific EDPB PDF: pypdf gives cleaner testcase labels.
    try:
        from pypdf import PdfReader

        reader = PdfReader(str(pdf_path))
        pages: list[str] = []
        for page in reader.pages:
            pages.append(page.extract_text() or "")
        non_empty = sum(1 for p in pages if p.strip())
        if non_empty > 0:
            return pages
    except Exception:
        pass

    # Fallback parser.
    try:
        import fitz  # type: ignore

        doc = fitz.open(pdf_path)
        return [page.get_text("text") for page in doc]
    except Exception:
        pass

    raise RuntimeError(f"Failed to parse PDF with both pypdf and pymupdf: {pdf_path}")


def normalize_line(text: str) -> str:
    text = text.replace("\u00a0", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def normalize_case_id(raw_id: str) -> str:
    candidate = raw_id.strip().replace(" ", "_").replace("-", "_").upper()
    if candidate.startswith("TC_"):
        suffix = re.sub(r"\D", "", candidate)
        if suffix:
            return f"TC-{int(suffix):02d}"
    return candidate


def normalize_testcase_label(prefix: str, serial: str) -> str:
    normalized_prefix = re.sub(r"[^A-Z0-9]+", "_", prefix.upper()).strip("_")
    normalized_serial = re.sub(r"[^0-9A-Z]+", "_", serial.upper()).strip("_")
    return f"{normalized_prefix}_{normalized_serial}"


def extract_article_refs(text: str) -> list[str]:
    refs: list[str] = []
    for match in ARTICLE_RE.finditer(text):
        art_num = str(int(match.group(1)))
        para = (match.group(2) or "").strip()
        ref = art_num if not para else f"{art_num}({para})"
        refs.append(ref)
    deduped: list[str] = []
    seen = set()
    for ref in refs:
        if ref in seen:
            continue
        seen.add(ref)
        deduped.append(ref)
    return deduped


def extract_cases_by_labels(pages: list[str]) -> list[dict]:
    cases: list[dict] = []
    current: dict | None = None
    active_article_context: list[str] = []

    for page_no, page_text in enumerate(pages, start=1):
        for raw_line in page_text.splitlines():
            line = normalize_line(raw_line)
            if not line:
                continue

            heading_like = bool(
                re.match(r"^\d+(?:\.\d+)*\s+", line)
                or "conditions for" in line.lower()
                or "right to" in line.lower()
                or "principle" in line.lower()
                or "lawfulness" in line.lower()
            )
            refs = extract_article_refs(line)
            if heading_like and refs:
                active_article_context = refs

            start_match = CASE_START_RE.search(line)
            if start_match:
                if current:
                    cases.append(current)

                prefix, serial, _level = start_match.groups()
                case_id = normalize_testcase_label(prefix, serial)
                lead_line = line[start_match.start() :].strip()
                title = line[start_match.end() :].strip(" -:\t")
                current = {
                    "id": case_id,
                    "title": title[:180],
                    "lead_line": lead_line,
                    "lines": [lead_line],
                    "pages": {page_no},
                    "context_articles": list(active_article_context),
                }
                continue

            if current is None:
                continue
            current["lines"].append(line)
            current["pages"].add(page_no)

    if current:
        cases.append(current)

    if not cases:
        return []

    # Merge duplicate IDs caused by PDF line wrapping/repetition across pages.
    merged: dict[str, dict] = {}
    for case in cases:
        cid = case["id"]
        if cid not in merged:
            merged[cid] = case
            continue
        merged[cid]["lines"].extend(case["lines"])
        merged[cid]["pages"].update(case["pages"])
        if not merged[cid].get("title") and case.get("title"):
            merged[cid]["title"] = case["title"]
        if not merged[cid].get("context_articles") and case.get("context_articles"):
            merged[cid]["context_articles"] = case["context_articles"]

    ordered = sorted(
        merged.values(),
        key=lambda c: (min(c["pages"]) if c["pages"] else 10**9, c["id"]),
    )
    return ordered


def extract_raw_cases(pages: list[str]) -> list[dict]:
    labeled_cases = extract_cases_by_labels(pages)
    if labeled_cases:
        return labeled_cases

    # Fallback segmentation by "Verification steps" blocks (common in the EDPB D2 format).
    marked_pages = [f"[[PAGE:{i + 1}]]\n{txt}" for i, txt in enumerate(pages)]
    all_text = "\n".join(marked_pages)
    parts = re.split(r"(?i)\bverification\s+steps\b", all_text)

    if len(parts) > 2:
        segmented: list[dict] = []
        for idx in range(1, len(parts)):
            pre = parts[idx - 1]
            post = parts[idx]
            context = pre[-1000:]
            block_text = f"{context}\nVerification steps\n{post[:8000]}"
            block_lines = [normalize_line(ln) for ln in block_text.splitlines() if normalize_line(ln)]

            raw_id = None
            for probe in reversed(block_lines[:20]):
                m = CASE_ID_RE.match(probe)
                if m:
                    raw_id = m.group(1)
                    break

            case_id = normalize_case_id(raw_id) if raw_id else f"TC-{idx:03d}"
            title = ""
            if raw_id:
                for probe in block_lines[:20]:
                    m = CASE_ID_RE.match(probe)
                    if m:
                        title = probe[m.end() :].strip(" -:\t")
                        break
            if not title:
                title = f"Verification block {idx}"

            page_hits = sorted(
                {
                    int(m.group(1))
                    for m in re.finditer(r"\[\[PAGE:(\d+)\]\]", block_text)
                    if m.group(1).isdigit()
                }
            )
            if not page_hits:
                page_hits = [1]

            segmented.append(
                {
                    "id": case_id,
                    "title": title[:180],
                    "lines": [ln for ln in block_lines if not ln.startswith("[[PAGE:")],
                    "pages": set(page_hits),
                }
            )

        if segmented:
            return segmented

    # Final fallback: keep one deterministic block to avoid hard crash.
    return [
        {
            "id": "TC-001",
            "title": "EDPB_D2_FALLBACK_CASE",
            "lines": [normalize_line(line) for line in all_text.splitlines() if normalize_line(line)],
            "pages": set(range(1, len(pages) + 1)),
        }
    ]


def detect_section(line: str) -> str | None:
    lowered = line.lower()
    for section, aliases in SECTION_ALIASES.items():
        if any(alias in lowered for alias in aliases):
            return section
    return None


def split_sections(lines: Iterable[str]) -> dict[str, list[str]]:
    buckets = {
        "preamble": [],
        "requirement": [],
        "audit_procedure": [],
        "evidence": [],
        "finding": [],
    }
    active = "preamble"
    for line in lines:
        detected = detect_section(line)
        if detected:
            active = detected
            continue
        buckets[active].append(line)
    return buckets


def to_steps(lines: list[str]) -> list[AuditProcedureStep]:
    steps: list[str] = []
    current = ""
    for line in lines:
        stripped = re.sub(r"^[\-\*\u2022]\s*", "", line).strip()
        numbered = re.sub(r"^\(?\d{1,2}\)?[.)\-:]\s*", "", stripped).strip()
        if not numbered:
            continue
        starts_new = bool(re.match(r"^\(?\d{1,2}\)?[.)\-:]", line)) or stripped.startswith(("-", "*", "\u2022"))
        if starts_new:
            if current:
                steps.append(current.strip())
            current = numbered
        else:
            if current:
                current = f"{current} {numbered}".strip()
            else:
                current = numbered
    if current:
        steps.append(current.strip())
    if not steps:
        # deterministic fallback from text order
        steps = [line for line in lines[:6] if len(line) > 15]
    normalized_steps = [s[:600] for s in steps if len(s.strip()) >= 3]
    return [AuditProcedureStep(order=i + 1, instruction=s) for i, s in enumerate(normalized_steps[:12])]


def to_evidence(lines: list[str]) -> list[EvidenceRequirement]:
    evidence_lines: list[str] = []
    for line in lines:
        cleaned = re.sub(r"^[\-\*\u2022]\s*", "", line).strip()
        cleaned = re.sub(r"^\(?\d{1,2}\)?[.)\-:]\s*", "", cleaned).strip()
        if cleaned:
            evidence_lines.append(cleaned)

    if not evidence_lines:
        return []

    deduped: list[str] = []
    seen = set()
    for item in evidence_lines:
        key = item.lower()
        if key in seen:
            continue
        seen.add(key)
        deduped.append(item)

    reqs: list[EvidenceRequirement] = []
    for idx, item in enumerate(deduped[:15], start=1):
        reqs.append(
            EvidenceRequirement(
                id=f"EV-{idx:02d}",
                description=item[:700],
                required=True,
                acceptable_artifacts=[],
            )
        )
    return reqs


def to_finding_criteria(lines: list[str], evidence: list[EvidenceRequirement]) -> list[FindingCriterion]:
    criteria: list[FindingCriterion] = []

    for idx, line in enumerate(lines, start=1):
        text = re.sub(r"^[\-\*\u2022]\s*", "", line).strip()
        if not text:
            continue
        if_condition = text
        if not text.lower().startswith("if "):
            if_condition = f"If {text[0].lower() + text[1:]}" if len(text) > 1 else f"If {text.lower()}"
        criteria.append(
            FindingCriterion(
                id=f"FC-{idx:02d}",
                if_condition=if_condition[:700],
                then_outcome="FAIL",
                judge_instruction="Mark the testcase as FAIL when this condition is true.",
            )
        )

    if not criteria:
        for idx, ev in enumerate(evidence, start=1):
            criteria.append(
                FindingCriterion(
                    id=f"FC-{idx:02d}",
                    if_condition=f"If required evidence '{ev.id}' is missing, contradictory, or unverifiable.",
                    then_outcome="FAIL",
                    judge_instruction="Return FAIL and list missing controls explicitly.",
                )
            )

    if not criteria:
        criteria.append(
            FindingCriterion(
                id="FC-01",
                if_condition="If no verifiable evidence is provided for the tested requirement.",
                then_outcome="FAIL",
                judge_instruction="Return FAIL due to evidence gap.",
            )
        )
    return criteria


def build_article_index(repo_root: Path) -> dict[str, str]:
    articles_root = repo_root / "packages" / "specs" / "legal" / "eu" / "gdpr" / "articles"
    index: dict[str, str] = {}
    for path in sorted(articles_root.glob("art_*.md")):
        m = re.search(r"art_(\d{3})\.md$", path.name)
        if not m:
            continue
        article_num = str(int(m.group(1)))
        index[article_num] = str(path.relative_to(repo_root)).replace("\\", "/")
    return index


def extract_article_mappings(text: str, article_index: dict[str, str]) -> list[GdprArticleMapping]:
    mappings: list[GdprArticleMapping] = []
    seen: set[str] = set()

    for match in ARTICLE_RE.finditer(text):
        art_num = str(int(match.group(1)))
        para = (match.group(2) or "").strip()
        key = f"{art_num}:{para}"
        if key in seen:
            continue
        seen.add(key)

        ref = art_num if not para else f"{art_num}({para})"
        path = article_index.get(art_num)
        snippet = text[max(0, match.start() - 60) : min(len(text), match.end() + 80)]
        mappings.append(
            GdprArticleMapping(
                article=ref,
                article_path=path,
                mapping_type="explicit" if path else "unmapped",
                source_snippet=normalize_line(snippet)[:240],
            )
        )
    return mappings


def self_correct_rule(rule: MasterAuditRule, case_text: str) -> MasterAuditRule:
    issues = list(rule.validation_issues)
    lines = [normalize_line(x) for x in case_text.splitlines() if normalize_line(x)]

    if not rule.requirement or len(rule.requirement.strip()) < 15:
        fallback_req = next((ln for ln in lines if len(ln) > 20), "Requirement could not be parsed automatically.")
        rule.requirement = fallback_req[:700]

    if not rule.audit_procedure:
        fallback_steps = [ln for ln in lines if re.search(r"\b(verify|check|confirm|inspect|review)\b", ln, re.I)]
        if not fallback_steps:
            fallback_steps = lines[:4]
        rule.audit_procedure = [
            AuditProcedureStep(order=i + 1, instruction=step[:600])
            for i, step in enumerate(fallback_steps[:6])
        ]

    if not rule.evidence_requirements:
        fallback_evidence = [
            ln
            for ln in lines
            if re.search(r"\b(log|record|policy|proof|document|evidence|contract)\b", ln, re.I)
        ]
        if fallback_evidence:
            rule.evidence_requirements = [
                EvidenceRequirement(id=f"EV-{i + 1:02d}", description=item[:700], required=True)
                for i, item in enumerate(fallback_evidence[:8])
            ]
        else:
            issues.append("No evidence block found; manual review required.")

    if not rule.finding_criteria:
        rule.finding_criteria = to_finding_criteria([], rule.evidence_requirements)

    if not rule.gdpr_article_mappings:
        issues.append("No explicit GDPR article references found; manual legal mapping required.")

    rule.validation_issues = issues
    return rule


def build_rule(raw_case: dict, article_index: dict[str, str]) -> MasterAuditRule:
    sections = split_sections(raw_case["lines"])
    full_text = "\n".join(raw_case["lines"])

    lead_line = raw_case.get("lead_line", "")
    requirement_lines = sections["requirement"] or ([lead_line] if lead_line else []) or sections["preamble"][:3]
    requirement = " ".join(requirement_lines).strip()[:900] if requirement_lines else ""
    if len(requirement) < 3:
        fallback = next((ln for ln in raw_case["lines"] if len(ln.strip()) >= 20), "")
        requirement = (fallback or "Requirement extraction incomplete; manual review required.")[:900]

    audit_steps = to_steps(sections["audit_procedure"] or sections["preamble"][:8])
    evidence = to_evidence(sections["evidence"])
    finding = to_finding_criteria(sections["finding"], evidence)
    article_mappings = extract_article_mappings(full_text, article_index)
    if not article_mappings:
        for ref in raw_case.get("context_articles", []):
            art_num_match = re.match(r"^(\d+)", ref)
            art_num = art_num_match.group(1) if art_num_match else ref
            article_mappings.append(
                GdprArticleMapping(
                    article=ref,
                    article_path=article_index.get(art_num),
                    mapping_type="context_inherited" if article_index.get(art_num) else "unmapped",
                    source_snippet="Inherited from nearest section heading containing GDPR article reference.",
                )
            )

    rule = MasterAuditRule(
        id=raw_case["id"],
        title=raw_case["title"],
        requirement=requirement or "Requirement missing after initial extraction.",
        audit_procedure=audit_steps,
        evidence_requirements=evidence,
        finding_criteria=finding,
        gdpr_article_mappings=article_mappings,
        source_pages=sorted(raw_case["pages"]),
        source_section=raw_case["title"] or raw_case["id"],
    )

    return self_correct_rule(rule, full_text)


def main() -> None:
    args = parse_args()
    base_dir = Path(__file__).resolve().parent
    repo_root = Path(args.repo_root).resolve()
    pdf_path = (base_dir / args.pdf_path).resolve()
    out_json = (base_dir / args.output_json).resolve()
    out_yaml = (base_dir / args.output_yaml).resolve()

    download_pdf(args.pdf_url, pdf_path)
    pages = extract_pages_text(pdf_path)
    raw_cases = extract_raw_cases(pages)
    if args.max_cases > 0:
        raw_cases = raw_cases[: args.max_cases]

    article_index = build_article_index(repo_root)
    rules = [build_rule(case, article_index) for case in raw_cases]

    mapped = sum(1 for rule in rules if rule.gdpr_article_mappings)
    unresolved = sum(1 for rule in rules if rule.validation_issues)
    catalog = MasterAuditCatalog(
        source_document=str(pdf_path),
        parser="pypdf|pymupdf-fallback",
        rules=rules,
        stats={
            "total_cases": len(rules),
            "cases_with_article_mapping": mapped,
            "cases_with_validation_issues": unresolved,
            "article_index_size": len(article_index),
        },
    )

    catalog.to_json_file(out_json)
    catalog.to_yaml_file(out_yaml)
    persisted = MasterAuditCatalog.from_file(out_json)

    print(f"[ok] extracted rules: {len(rules)}")
    print(f"[ok] persisted rules: {len(persisted.rules)}")
    print(f"[ok] json: {out_json}")
    print(f"[ok] yaml: {out_yaml}")
    print(f"[ok] mapped cases: {mapped} / {len(rules)}")
    print(f"[ok] cases requiring manual review: {unresolved}")


if __name__ == "__main__":
    main()
