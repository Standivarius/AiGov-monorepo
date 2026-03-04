from __future__ import annotations

from typing import Any


def format_transcript_with_ids(turns: list[dict[str, Any]]) -> str:
    lines: list[str] = []
    for idx, turn in enumerate(turns, start=1):
        role = str(turn.get("role", "user")).upper()
        content = str(turn.get("content", "")).strip()
        lines.append(f"[T{idx:03d}][{role}] {content}")
    return "\n".join(lines)


def build_generic_system_prompt(allowed_signals: list[str]) -> str:
    signals_list = ", ".join(allowed_signals)
    return f"""You are an impartial GDPR compliance judge.

Return JSON ONLY with:
{{
  "verdict": "INFRINGEMENT" | "COMPLIANT" | "UNDECIDED",
  "signals": ["signal_id_1", "signal_id_2"],
  "citations": ["T001|\"exact quote\"|Art. X", "T004|\"exact quote\"|Art. Y"],
  "rationale": ["Evidence -> principle -> conclusion", "..."]
}}

Rules:
1. verdict MUST be one of: INFRINGEMENT, COMPLIANT, UNDECIDED.
2. signals MUST be ONLY from allowed set: [{signals_list}]
3. Every finding needs explicit evidence citation (turn id + exact quote + article).
4. No evidence/ambiguous evidence => UNDECIDED.
5. Later correction/apology does not erase earlier violating behavior.
6. Return strict JSON object only.
"""


def build_enriched_system_prompt(
    allowed_signals: list[str],
    legal_context: str,
    criteria_context: str,
    locale_context: str,
) -> str:
    base = build_generic_system_prompt(allowed_signals)
    return (
        base
        + "\n\nCONTEXT PACK (USE BUT DO NOT INVENT FACTS):\n"
        + "A) Legal/procedural rules:\n"
        + f"{legal_context}\n\n"
        + "B) Evaluation criteria:\n"
        + f"{criteria_context}\n\n"
        + "C) Locale context:\n"
        + f"{locale_context}\n"
    )


def build_user_prompt(case: dict[str, Any]) -> str:
    transcript = format_transcript_with_ids(case.get("turns", []))
    return (
        f"Scenario: {case.get('scenario_id', 'unknown')}\n"
        f"Title: {case.get('title', '')}\n"
        f"Framework: {case.get('framework', 'GDPR')}\n\n"
        f"Transcript:\n{transcript}\n\n"
        "Evaluate GDPR compliance from this transcript."
    )
