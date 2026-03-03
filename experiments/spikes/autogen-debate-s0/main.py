from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
import uuid
from pathlib import Path
from typing import Any

import chromadb
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.teams import SelectorGroupChat
from autogen_ext.models.openai import OpenAIChatCompletionClient
from pypdf import PdfReader

from schemas import JudgeVerdict, MasterAuditCatalog, MasterAuditRule


class DirectoryRetriever:
    def __init__(self, docs_dir: Path, persist_dir: Path, collection_name: str) -> None:
        self.docs_dir = docs_dir
        self.persist_dir = persist_dir
        self.client = chromadb.PersistentClient(path=str(persist_dir))
        self.collection = self.client.get_or_create_collection(collection_name)

    def index(self, rebuild: bool = False) -> None:
        self.persist_dir.mkdir(parents=True, exist_ok=True)
        self.docs_dir.mkdir(parents=True, exist_ok=True)

        if rebuild:
            self.client.delete_collection(self.collection.name)
            self.collection = self.client.get_or_create_collection(self.collection.name)

        if self.collection.count() > 0 and not rebuild:
            return

        ids: list[str] = []
        docs: list[str] = []
        metadatas: list[dict[str, Any]] = []

        for path in sorted(self.docs_dir.rglob("*")):
            if not path.is_file():
                continue
            content = self._read_text(path)
            if not content.strip():
                continue
            for idx, chunk in enumerate(self._chunk_text(content), start=1):
                chunk_id = f"{path.stem}-{idx}-{uuid.uuid4().hex[:8]}"
                ids.append(chunk_id)
                docs.append(chunk)
                metadatas.append({"source": str(path), "chunk_index": idx})

        if ids:
            self.collection.add(ids=ids, documents=docs, metadatas=metadatas)

    def query(self, query_text: str, n_results: int = 4) -> str:
        if self.collection.count() == 0:
            return "No indexed documents found."
        result = self.collection.query(query_texts=[query_text], n_results=n_results)
        docs = result.get("documents", [[]])[0]
        metas = result.get("metadatas", [[]])[0]
        snippets: list[str] = []
        for i, (doc, meta) in enumerate(zip(docs, metas), start=1):
            source = meta.get("source", "unknown")
            chunk = meta.get("chunk_index", "?")
            snippets.append(f"[{i}] source={source} chunk={chunk}\n{doc[:700]}")
        return "\n\n".join(snippets) if snippets else "No relevant evidence found."

    @staticmethod
    def _chunk_text(text: str, size: int = 1200, overlap: int = 120) -> list[str]:
        text = re.sub(r"\s+", " ", text).strip()
        if not text:
            return []
        chunks: list[str] = []
        start = 0
        while start < len(text):
            end = min(len(text), start + size)
            chunks.append(text[start:end])
            if end == len(text):
                break
            start = max(0, end - overlap)
        return chunks

    @staticmethod
    def _read_text(path: Path) -> str:
        suffix = path.suffix.lower()
        if suffix in {".txt", ".md", ".json", ".yaml", ".yml", ".csv"}:
            return path.read_text(encoding="utf-8", errors="ignore")
        if suffix == ".pdf":
            try:
                reader = PdfReader(str(path))
                return "\n".join(page.extract_text() or "" for page in reader.pages)
            except Exception:
                return ""
        return ""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="AutoGen courtroom debate grounded by extracted EDPB rules.")
    parser.add_argument(
        "--rules-file",
        default="data/master_audit_rules.json",
        help="Path to extracted master rules file (JSON/YAML).",
    )
    parser.add_argument("--test-case-id", default=None, help="Rule id to load, defaults to first rule in catalog.")
    parser.add_argument(
        "--task",
        default="Begin the GDPR audit specifically focusing on Data Processing Agreements and sub-processor tracking.",
        help="Initial user trigger.",
    )
    parser.add_argument("--rebuild-index", action="store_true", help="Rebuild Chroma indexes from docs folders.")
    return parser.parse_args()


def load_rule(base_dir: Path, rules_file: str, test_case_id: str | None) -> MasterAuditRule:
    catalog_path = (base_dir / rules_file).resolve()
    catalog = MasterAuditCatalog.from_file(catalog_path)
    return catalog.get_rule(test_case_id)


def build_model_client() -> OpenAIChatCompletionClient:
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")

    if openrouter_key:
        base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
        model = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o")
        return OpenAIChatCompletionClient(
            model=model,
            api_key=openrouter_key,
            base_url=base_url,
            model_info={
                "vision": False,
                "function_calling": True,
                "json_output": True,
                "family": "unknown",
                "structured_output": True,
            },
        )

    if openai_key:
        model = os.getenv("OPENAI_MODEL", "gpt-4o")
        return OpenAIChatCompletionClient(model=model, api_key=openai_key)

    raise RuntimeError("Set OPENROUTER_API_KEY or OPENAI_API_KEY before running main.py.")


def _format_rule_context(rule: MasterAuditRule) -> str:
    audit = "\n".join([f"{s.order}. {s.instruction}" for s in rule.audit_procedure]) or "(none parsed)"
    evidence = "\n".join([f"- {e.id}: {e.description}" for e in rule.evidence_requirements]) or "- (none parsed)"
    findings = (
        "\n".join([f"- {c.id}: IF {c.if_condition} THEN {c.then_outcome}" for c in rule.finding_criteria])
        or "- (none parsed)"
    )
    articles = ", ".join([m.article for m in rule.gdpr_article_mappings]) or "No explicit article mapping found"
    return (
        f"Test Case: {rule.id}\n"
        f"Title: {rule.title}\n"
        f"Requirement: {rule.requirement}\n"
        f"Mapped GDPR Articles: {articles}\n\n"
        f"Audit Procedure:\n{audit}\n\n"
        f"Evidence Requirements:\n{evidence}\n\n"
        f"Finding Criteria:\n{findings}\n"
    )


def auditor_system_message(rule: MasterAuditRule) -> str:
    return (
        "You are the Lead GDPR Auditor (Prosecutor).\n"
        "You must aggressively challenge the Defender against the loaded test case only.\n"
        "Never guess. Before each challenge, call your retrieval tool to cite legal/manual evidence.\n"
        "Demand concrete documents, logs, and controls from the Defender.\n"
        "Reject vague assurances.\n\n"
        + _format_rule_context(rule)
    )


def defender_system_message() -> str:
    return (
        "You are the Client Defense Architect.\n"
        "You are blind to the auditor manual and must rely only on docs_client_evidence via your retrieval tool.\n"
        "If evidence is missing, explicitly admit it.\n"
        "Do not invent controls, logs, or contracts.\n"
    )


def judge_system_message(rule: MasterAuditRule) -> str:
    finding_lines = "\n".join(
        [
            f"- {c.id}: IF {c.if_condition} THEN {c.then_outcome}. Judge instruction: {c.judge_instruction}"
            for c in rule.finding_criteria
        ]
    )
    return (
        "You are the Impartial GDPR Judge.\n"
        "You are not allowed to invent new arguments.\n"
        "Evaluate only whether the Defender supplied evidence required by the testcase and whether finding criteria were triggered.\n"
        "Output only a strict JSON object with keys:\n"
        '{"audited_topic": string, "gdpr_article": string, "compliance_score_0_to_100": integer, '
        '"evidence_found": string, "missing_controls": string, "severity": "Low|Medium|High", '
        '"canonical_verdict": "INFRINGEMENT|COMPLIANT|UNDECIDED"}\n'
        "If evidence is materially missing, canonical_verdict must be UNDECIDED or INFRINGEMENT.\n\n"
        f"Finding Criteria:\n{finding_lines}\n"
    )


def extract_json(text: str) -> str:
    text = text.strip()
    fenced = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, flags=re.DOTALL)
    if fenced:
        return fenced.group(1)
    brace = re.search(r"(\{.*\})", text, flags=re.DOTALL)
    if brace:
        return brace.group(1)
    raise ValueError("No JSON object found in judge response.")


def derive_canonical_verdict(score: int, missing_controls: str, severity: str) -> str:
    if not missing_controls.strip() and score >= 80 and severity == "Low":
        return "COMPLIANT"
    if score < 50 or severity == "High":
        return "INFRINGEMENT"
    return "UNDECIDED"


def validate_judge_output(raw_content: str) -> JudgeVerdict:
    payload = json.loads(extract_json(raw_content))
    if "canonical_verdict" not in payload:
        payload["canonical_verdict"] = derive_canonical_verdict(
            int(payload.get("compliance_score_0_to_100", 0)),
            str(payload.get("missing_controls", "")),
            str(payload.get("severity", "Medium")),
        )
    return JudgeVerdict.model_validate(payload)


def selector_function(messages: list[Any]) -> str:
    order = ["Lead_Auditor", "Client_Defender", "Lead_Auditor", "Client_Defender", "GDPR_Judge"]
    spoken = [m for m in messages if getattr(m, "source", None) in {"Lead_Auditor", "Client_Defender", "GDPR_Judge"}]
    index = len(spoken)
    if index < len(order):
        return order[index]
    return "GDPR_Judge"


async def run() -> None:
    args = parse_args()
    base_dir = Path(__file__).resolve().parent
    rule = load_rule(base_dir, args.rules_file, args.test_case_id)

    auditor_docs = base_dir / "docs_auditor_manual"
    defender_docs = base_dir / "docs_client_evidence"
    auditor_retriever = DirectoryRetriever(
        docs_dir=auditor_docs,
        persist_dir=base_dir / "chroma" / "auditor",
        collection_name="auditor_manual",
    )
    defender_retriever = DirectoryRetriever(
        docs_dir=defender_docs,
        persist_dir=base_dir / "chroma" / "defender",
        collection_name="client_evidence",
    )
    auditor_retriever.index(rebuild=args.rebuild_index)
    defender_retriever.index(rebuild=args.rebuild_index)

    def retrieve_auditor_manual(query: str) -> str:
        return auditor_retriever.query(query)

    def retrieve_client_evidence(query: str) -> str:
        return defender_retriever.query(query)

    model_client = build_model_client()
    try:
        auditor = AssistantAgent(
            name="Lead_Auditor",
            model_client=model_client,
            system_message=auditor_system_message(rule),
            tools=[retrieve_auditor_manual],
            description="Lead GDPR auditor that attacks compliance based on audit manual evidence.",
        )
        defender = AssistantAgent(
            name="Client_Defender",
            model_client=model_client,
            system_message=defender_system_message(),
            tools=[retrieve_client_evidence],
            description="Client defender restricted to client evidence repository.",
        )
        judge = AssistantAgent(
            name="GDPR_Judge",
            model_client=model_client,
            system_message=judge_system_message(rule),
            description="Impartial judge constrained to testcase finding criteria.",
        )

        team = SelectorGroupChat(
            [auditor, defender, judge],
            model_client=model_client,
            selector_func=selector_function,
            termination_condition=MaxMessageTermination(max_messages=5),
        )
        result = await team.run(task=args.task)
    finally:
        await model_client.close()

    judge_messages = [m for m in result.messages if getattr(m, "source", None) == "GDPR_Judge"]
    if not judge_messages:
        raise RuntimeError("No judge message found in conversation output.")

    verdict = validate_judge_output(str(judge_messages[-1].content))
    print(verdict.model_dump_json(indent=2))


if __name__ == "__main__":
    asyncio.run(run())

