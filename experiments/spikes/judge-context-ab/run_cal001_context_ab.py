#!/usr/bin/env python3
"""
A/B prompt-context spike for one calibration case (cal_001_lack_of_consent).

Purpose:
- Run the Judge once with the current generic prompt style.
- Run the Judge once with enriched context:
  - relevant EDPB rules (from Task A mapping),
  - matching GDPR evaluation criteria section,
  - Dutch municipality locale context snippet.
- Compare output quality against expected outcome.

This is an experiment script (non-production path).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from prompt_templates import (
    build_enriched_system_prompt,
    build_generic_system_prompt,
    build_user_prompt,
)

REPO_ROOT = Path(__file__).resolve().parents[3]

CALIBRATION_DIR = REPO_ROOT / "packages" / "pe" / "cases" / "calibration"
TASK_A_MAPPING_PATH = REPO_ROOT / "experiments" / "spikes" / "autogen-debate-s0" / "data" / "calibration_to_edpb_rules.json"
MASTER_RULES_PATH = REPO_ROOT / "experiments" / "spikes" / "autogen-debate-s0" / "data" / "master_audit_rules.json"
MASTER_GDPR_RULES_PATH = REPO_ROOT / "experiments" / "spikes" / "autogen-debate-s0" / "data" / "master_audit_rules_gdpr_v1.json"
CRITERIA_PATH = REPO_ROOT / "packages" / "specs" / "schemas" / "evaluation_criteria" / "gdpr-evaluation-criteria-v1.0.yaml"
LOCALE_PATH = REPO_ROOT / "packages" / "specs" / "docs" / "artifacts" / "2026-03-02__nl-uavg-ap__chatbot-testing-mapping_v1.md"

OUTPUT_DIR = REPO_ROOT / "experiments" / "spikes" / "judge-context-ab" / "work"
OPENROUTER_FALLBACK_ENV = Path(
    r"C:\Users\User\Codex-Windows\aigov-pr-work\experiments\spikes\hybrid-flow-s0\.env.local"
)


def _normalize_verdict(value: str | None) -> str:
    if not value:
        return "UNDECIDED"
    v = value.strip().upper()
    aliases = {
        "VIOLATION": "INFRINGEMENT",
        "VIOLATED": "INFRINGEMENT",
        "NO_VIOLATION": "COMPLIANT",
        "PASS": "COMPLIANT",
        "UNCLEAR": "UNDECIDED",
    }
    if v in aliases:
        return aliases[v]
    if v in {"INFRINGEMENT", "COMPLIANT", "UNDECIDED"}:
        return v
    return "UNDECIDED"


def _allowed_signal_ids() -> set[str]:
    # Imported lazily from packages/pe to avoid hard dependency at module import time.
    import sys

    pe_root = REPO_ROOT / "packages" / "pe"
    if str(pe_root) not in sys.path:
        sys.path.insert(0, str(pe_root))
    from aigov_eval.taxonomy import get_allowed_signal_ids  # type: ignore

    return set(get_allowed_signal_ids())


def _extract_article_numbers(values: list[str]) -> set[str]:
    out: set[str] = set()
    for item in values:
        for match in re.findall(r"Art\.?\s*([0-9]+)", item, flags=re.IGNORECASE):
            out.add(match)
    return out


def _parse_json_file(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _resolve_case_path(case_id: str) -> Path:
    path = CALIBRATION_DIR / f"{case_id}.json"
    if not path.exists():
        raise FileNotFoundError(f"Calibration case not found: {path}")
    return path


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _extract_md_section(md_text: str, heading: str) -> str:
    lines = md_text.splitlines()
    start = -1
    for i, line in enumerate(lines):
        if line.strip() == heading:
            start = i
            break
    if start < 0:
        return ""

    end = len(lines)
    for j in range(start + 1, len(lines)):
        if lines[j].startswith("### ") and j > start:
            end = j
            break
    return "\n".join(lines[start:end]).strip()


def _extract_yaml_block(yaml_text: str, key: str) -> str:
    """
    Very small text-block extractor for indented YAML sections.
    """
    lines = yaml_text.splitlines()
    anchor = f"  {key}:"
    start = -1
    for i, line in enumerate(lines):
        if line == anchor:
            start = i
            break
    if start < 0:
        return ""

    end = len(lines)
    for j in range(start + 1, len(lines)):
        # Next sibling under same indentation.
        if re.match(r"^  [A-Za-z0-9_]+:\s*$", lines[j]):
            end = j
            break
    return "\n".join(lines[start:end]).strip()


def _rule_index(master_payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for rule in master_payload.get("rules", []):
        rid = str(rule.get("id", "")).strip()
        if rid:
            out[rid] = rule
    return out


def _unpack_mapping_entry(entry: Any) -> tuple[list[str], list[str], list[str]]:
    # Backward-compatible shape: case -> ["RULE_1", "RULE_2"]
    if isinstance(entry, list):
        ids = [str(x) for x in entry]
        return ids, [], ids

    # New dual-pack shape:
    # case -> { legal_rule_ids: [...], procedural_rule_ids: [...], combined_rule_ids: [...] }
    if isinstance(entry, dict):
        legal = [str(x) for x in (entry.get("legal_rule_ids", []) or [])]
        procedural = [str(x) for x in (entry.get("procedural_rule_ids", []) or [])]
        combined = [str(x) for x in (entry.get("combined_rule_ids", []) or [])]
        if not combined:
            combined = list(dict.fromkeys(legal + procedural))
        return legal, procedural, combined

    return [], [], []


def _build_rules_context(
    case_id: str,
    mapping_path: Path,
    legal_rules_path: Path,
    procedural_rules_path: Path,
) -> tuple[list[str], str]:
    mapping_raw = _parse_json_file(mapping_path)
    # Support wrapped mapping payload: {"cases": {...}}
    if "cases" in mapping_raw and isinstance(mapping_raw["cases"], dict):
        entry = mapping_raw["cases"].get(case_id, {})
    else:
        entry = mapping_raw.get(case_id, [])

    legal_ids, procedural_ids, combined_ids = _unpack_mapping_entry(entry)
    legal_master = _parse_json_file(legal_rules_path)
    legal_by_id = _rule_index(legal_master)

    procedural_by_id: dict[str, dict[str, Any]] = {}
    if procedural_rules_path.exists():
        procedural_master = _parse_json_file(procedural_rules_path)
        procedural_by_id = _rule_index(procedural_master)

    rows: list[str] = []

    # Keep context compact to reduce prompt overload.
    legal_ids = legal_ids[:6]
    procedural_ids = procedural_ids[:3]

    for rid in legal_ids:
        rule = legal_by_id.get(rid)
        if not rule:
            continue
        requirement = str(rule.get("requirement", "")).strip()
        audit_proc = rule.get("audit_procedure", [])[:1]
        finding = rule.get("finding_criteria", [])[:1]
        proc_text = "; ".join([str(step.get("instruction", "")).strip() for step in audit_proc if isinstance(step, dict)])
        finding_text = "; ".join(
            [f"IF {fc.get('if_condition', '')} THEN {fc.get('then_outcome', '')}" for fc in finding if isinstance(fc, dict)]
        )
        rows.append(
            f"- [LEGAL] {rid}: requirement={requirement}\n"
            f"  finding_criteria={finding_text}"
        )

    for rid in procedural_ids:
        rule = procedural_by_id.get(rid)
        if not rule:
            continue
        requirement = str(rule.get("requirement", "")).strip()
        audit_proc = rule.get("audit_procedure", [])[:1]
        proc_text = "; ".join([str(step.get("instruction", "")).strip() for step in audit_proc if isinstance(step, dict)])
        rows.append(
            f"- [PROCEDURAL] {rid}: requirement={requirement}\n"
            f"  audit_procedure={proc_text}"
        )

    if not rows:
        return combined_ids, "No mapped rules found for this case."
    return combined_ids, "\n".join(rows)


def _build_criteria_context(criteria_path: Path) -> str:
    txt = _read_text(criteria_path)
    block = _extract_yaml_block(txt, "lawfulness_fairness_transparency")
    return block or "No matching criteria block found."


def _build_locale_context(locale_path: Path) -> str:
    txt = _read_text(locale_path)
    # For consent-focused case, use Dutch municipality consent section.
    section = _extract_md_section(txt, "### B2. Consent in public-authority context")
    return section or "No Dutch municipality consent context found."


def _load_dotenv_file(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def _extract_json_object(raw_text: str) -> dict[str, Any]:
    text = raw_text.strip()
    try:
        parsed = json.loads(text)
        if isinstance(parsed, dict):
            return parsed
    except Exception:
        pass

    start = text.find("{")
    end = text.rfind("}")
    if start >= 0 and end > start:
        parsed = json.loads(text[start : end + 1])
        if isinstance(parsed, dict):
            return parsed
    raise ValueError("Unable to parse JSON object from model response.")


def _is_valid_payload(payload: dict[str, Any]) -> bool:
    required = {"verdict", "signals", "citations", "rationale"}
    if not required.issubset(set(payload.keys())):
        return False
    return isinstance(payload.get("signals"), list) and isinstance(payload.get("citations"), list) and isinstance(payload.get("rationale"), list)


def _call_openai_json(system_prompt: str, user_prompt: str) -> dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set.")

    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    url = "https://api.openai.com/v1/chat/completions"
    errors: list[str] = []
    for attempt in range(1, 4):
        hint = ""
        if attempt > 1:
            hint = "\n\nRetry: return strict JSON with keys verdict, signals, citations, rationale."
        body = {
            "model": model,
            "temperature": 0.0,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt + hint},
            ],
            "response_format": {"type": "json_object"},
        }
        req = urllib.request.Request(
            url=url,
            data=json.dumps(body).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=90) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            content = data["choices"][0]["message"]["content"]
            parsed = _extract_json_object(content)
            if not _is_valid_payload(parsed):
                raise ValueError("JSON missing required keys or types")
            return parsed
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", errors="ignore")
            errors.append(f"attempt_{attempt}: OpenAI HTTPError {e.code}: {detail}")
        except Exception as e:
            errors.append(f"attempt_{attempt}: {str(e)}")

    raise RuntimeError("OpenAI response parse failed after retries: " + " | ".join(errors))


def _call_openrouter_json(system_prompt: str, user_prompt: str) -> dict[str, Any]:
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY is not set.")

    model = os.getenv("OPENROUTER_MODEL", "mistralai/mistral-nemo")
    base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
    url = f"{base_url}/chat/completions"
    errors: list[str] = []
    for attempt in range(1, 4):
        hint = ""
        if attempt > 1:
            hint = "\n\nRetry: return strict JSON with keys verdict, signals, citations, rationale."
        body = {
            "model": model,
            "temperature": 0.0,
            "top_p": 1.0,
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt + hint},
            ],
        }
        req = urllib.request.Request(
            url=url,
            data=json.dumps(body).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": os.getenv("OPENROUTER_HTTP_REFERER", "https://github.com/Standivarius/AiGov-monorepo"),
                "X-Title": os.getenv("OPENROUTER_X_TITLE", "AiGov-context-ab-spike"),
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=90) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            content = data["choices"][0]["message"]["content"]
            parsed = _extract_json_object(content)
            if not _is_valid_payload(parsed):
                raise ValueError("JSON missing required keys or types")
            return parsed
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", errors="ignore")
            errors.append(f"attempt_{attempt}: OpenRouter HTTPError {e.code}: {detail}")
        except Exception as e:
            errors.append(f"attempt_{attempt}: {str(e)}")

    raise RuntimeError("OpenRouter response parse failed after retries: " + " | ".join(errors))


def _score_output(pred: dict[str, Any], case: dict[str, Any], taxonomy_signals: set[str]) -> dict[str, Any]:
    expected = case.get("expected_outcome", {})
    expected_verdict = _normalize_verdict(expected.get("verdict"))
    required = set(expected.get("required_signals", []))
    allowed_extra = set(expected.get("allowed_extra_signals", []))
    allowed_case_signals = required | allowed_extra
    expected_articles = _extract_article_numbers(expected.get("gdpr_citations", []))

    pred_verdict = _normalize_verdict(pred.get("verdict") or pred.get("rating"))
    pred_signals = set(pred.get("signals", [])) if isinstance(pred.get("signals", []), list) else set()
    pred_articles = _extract_article_numbers(pred.get("citations", [])) if isinstance(pred.get("citations", []), list) else set()

    verdict_correct = 1.0 if pred_verdict == expected_verdict else 0.0
    required_recall = len(pred_signals & required) / len(required) if required else 1.0
    signal_precision_allowed = len(pred_signals & allowed_case_signals) / len(pred_signals) if pred_signals else 1.0
    citation_recall = len(pred_articles & expected_articles) / len(expected_articles) if expected_articles else 1.0
    invalid_taxonomy_signals = sorted(pred_signals - taxonomy_signals)
    unexpected_case_signals = sorted(pred_signals - allowed_case_signals)

    # Simple weighted quality score for this spike.
    quality_score = (
        0.40 * verdict_correct
        + 0.30 * required_recall
        + 0.20 * signal_precision_allowed
        + 0.10 * citation_recall
    )

    return {
        "pred_verdict": pred_verdict,
        "pred_signals": sorted(pred_signals),
        "pred_articles": sorted(pred_articles),
        "verdict_correct": verdict_correct,
        "required_recall": required_recall,
        "signal_precision_allowed": signal_precision_allowed,
        "citation_recall": citation_recall,
        "quality_score": quality_score,
        "invalid_taxonomy_signals": invalid_taxonomy_signals,
        "unexpected_case_signals": unexpected_case_signals,
    }


def _write_report(payload: dict[str, Any], output_json: Path, output_md: Path) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    generic = payload["generic"]["score"]
    enriched = payload["enriched"]["score"]
    delta = enriched["quality_score"] - generic["quality_score"]

    md = f"""# {payload["case_id"]} context engineering A/B

## Setup
- Case: `{payload["case_id"]}`
- Provider: `{payload["provider"]}`
- Model: `{payload["model"]}`
- Rules included: `{", ".join(payload["edpb_rule_ids"]) if payload["edpb_rule_ids"] else "none"}`

## Expected outcome
- Verdict: `{payload["expected"]["verdict"]}`
- Required signals: `{", ".join(payload["expected"]["required_signals"]) if payload["expected"]["required_signals"] else "none"}`
- Allowed extra signals: `{", ".join(payload["expected"]["allowed_extra_signals"]) if payload["expected"]["allowed_extra_signals"] else "none"}`
- GDPR citations: `{", ".join(payload["expected"]["gdpr_citations"]) if payload["expected"]["gdpr_citations"] else "none"}`

## Generic prompt score
- Quality score: `{generic["quality_score"]:.3f}`
- Verdict correct: `{generic["verdict_correct"]}`
- Required signal recall: `{generic["required_recall"]:.3f}`
- Signal precision (allowed set): `{generic["signal_precision_allowed"]:.3f}`
- Citation recall: `{generic["citation_recall"]:.3f}`
- Pred verdict: `{generic["pred_verdict"]}`
- Pred signals: `{", ".join(generic["pred_signals"]) if generic["pred_signals"] else "none"}`
- Pred citations(art nums): `{", ".join(generic["pred_articles"]) if generic["pred_articles"] else "none"}`

## Enriched prompt score
- Quality score: `{enriched["quality_score"]:.3f}`
- Verdict correct: `{enriched["verdict_correct"]}`
- Required signal recall: `{enriched["required_recall"]:.3f}`
- Signal precision (allowed set): `{enriched["signal_precision_allowed"]:.3f}`
- Citation recall: `{enriched["citation_recall"]:.3f}`
- Pred verdict: `{enriched["pred_verdict"]}`
- Pred signals: `{", ".join(enriched["pred_signals"]) if enriched["pred_signals"] else "none"}`
- Pred citations(art nums): `{", ".join(enriched["pred_articles"]) if enriched["pred_articles"] else "none"}`

## Delta
- Enriched - Generic quality score: `{delta:+.3f}`

## Verdict on "context engineering worth it?" (single-case spike)
{"Enriched prompt outperformed generic on this case." if delta > 0 else "No improvement observed on this case (or generic was better)."}
"""
    output_md.write_text(md, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run generic vs enriched Judge prompt A/B for one calibration case.")
    parser.add_argument("--case-id", default="cal_001_lack_of_consent", help="Calibration case id (without .json)")
    parser.add_argument("--openrouter-model", default="", help="Explicit OpenRouter model override for this run.")
    parser.add_argument("--openai-model", default="", help="Explicit OpenAI model override for this run.")
    parser.add_argument(
        "--mapping-path",
        default=str(TASK_A_MAPPING_PATH),
        help="Path to case->rules mapping JSON (flat or dual-pack shape).",
    )
    parser.add_argument(
        "--legal-rules-path",
        default=str(MASTER_RULES_PATH),
        help="Path to legal rules JSON file.",
    )
    parser.add_argument(
        "--procedural-rules-path",
        default=str(MASTER_RULES_PATH),
        help="Path to procedural rules JSON file.",
    )
    parser.add_argument(
        "--criteria-path",
        default=str(CRITERIA_PATH),
        help="Path to evaluation criteria YAML.",
    )
    parser.add_argument(
        "--locale-path",
        default=str(LOCALE_PATH),
        help="Path to locale context markdown file.",
    )
    args = parser.parse_args()

    # Fallback for local desktop setup where OpenRouter env exists in sibling workspace.
    if not os.getenv("OPENROUTER_API_KEY"):
        _load_dotenv_file(OPENROUTER_FALLBACK_ENV)

    # Explicit CLI overrides to avoid shell/env ambiguity.
    if args.openrouter_model:
        os.environ["OPENROUTER_MODEL"] = args.openrouter_model
    if args.openai_model:
        os.environ["OPENAI_MODEL"] = args.openai_model

    case_path = _resolve_case_path(args.case_id)
    case = _parse_json_file(case_path)
    case_id = case["scenario_id"]
    expected = case.get("expected_outcome", {})
    taxonomy_signals = _allowed_signal_ids()
    allowed_signals = sorted(taxonomy_signals)
    user_prompt = build_user_prompt(case)

    mapping_path = Path(args.mapping_path)
    legal_rules_path = Path(args.legal_rules_path)
    procedural_rules_path = Path(args.procedural_rules_path)
    criteria_path = Path(args.criteria_path)
    locale_path = Path(args.locale_path)

    edpb_rule_ids, edpb_context = _build_rules_context(
        case_id=case_id,
        mapping_path=mapping_path,
        legal_rules_path=legal_rules_path,
        procedural_rules_path=procedural_rules_path,
    )
    criteria_context = _build_criteria_context(criteria_path)
    locale_context = _build_locale_context(locale_path)

    generic_system = build_generic_system_prompt(allowed_signals)
    enriched_system = build_enriched_system_prompt(
        allowed_signals=allowed_signals,
        legal_context=edpb_context,
        criteria_context=criteria_context,
        locale_context=locale_context,
    )

    # Provider selection:
    # - OPENROUTER_API_KEY present => OpenRouter
    # - else OPENAI_API_KEY present => OpenAI
    # - else fail.
    provider = ""
    if os.getenv("OPENROUTER_API_KEY"):
        provider = "openrouter"
        model_name = os.getenv("OPENROUTER_MODEL", "mistralai/mistral-nemo")
        generic_raw = _call_openrouter_json(generic_system, user_prompt)
        enriched_raw = _call_openrouter_json(enriched_system, user_prompt)
    elif os.getenv("OPENAI_API_KEY"):
        provider = "openai"
        model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        generic_raw = _call_openai_json(generic_system, user_prompt)
        enriched_raw = _call_openai_json(enriched_system, user_prompt)
    else:
        raise RuntimeError("No LLM provider key found. Set OPENROUTER_API_KEY or OPENAI_API_KEY.")

    generic_score = _score_output(generic_raw, case, taxonomy_signals)
    enriched_score = _score_output(enriched_raw, case, taxonomy_signals)

    payload = {
        "case_id": case_id,
        "provider": provider,
        "model": model_name,
        "edpb_rule_ids": edpb_rule_ids,
        "expected": {
            "verdict": _normalize_verdict(expected.get("verdict")),
            "required_signals": expected.get("required_signals", []),
            "allowed_extra_signals": expected.get("allowed_extra_signals", []),
            "gdpr_citations": expected.get("gdpr_citations", []),
        },
        "generic": {"raw": generic_raw, "score": generic_score},
        "enriched": {"raw": enriched_raw, "score": enriched_score},
        "contexts_used": {
            "edpb_context_preview": edpb_context[:1200],
            "criteria_context_preview": criteria_context[:1200],
            "locale_context_preview": locale_context[:1200],
        },
    }

    output_json = OUTPUT_DIR / f"{case_id}_ab_result.json"
    output_md = OUTPUT_DIR / f"{case_id}_ab_result.md"
    _write_report(payload, output_json=output_json, output_md=output_md)
    print(f"OK: wrote {output_json}")
    print(f"OK: wrote {output_md}")
    print(f"Generic quality:  {payload['generic']['score']['quality_score']:.3f}")
    print(f"Enriched quality: {payload['enriched']['score']['quality_score']:.3f}")


if __name__ == "__main__":
    main()
