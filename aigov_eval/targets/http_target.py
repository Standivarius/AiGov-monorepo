"""HTTP target adapter for TargetLab RAG service."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any, Dict, List

from .base import TargetAdapter


DEFAULT_BASE_URL = "http://localhost:8000"


class HttpTargetAdapter(TargetAdapter):
    name = "http"

    def __init__(self, scenario: Dict[str, Any], config: Dict[str, Any]) -> None:
        super().__init__(scenario, config)
        self.base_url = str(config.get("base_url") or DEFAULT_BASE_URL).rstrip("/")
        self.leak_mode = str(config.get("leak_mode") or "strict")
        self.leak_profile = str(config.get("leak_profile") or "none")
        self.use_llm = bool(config.get("use_llm", False))
        self.session_id = str(config.get("session_id") or config.get("run_id") or "aigov-eval")

    def respond(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        last_user = _last_user_message(messages)
        payload = {
            "message": last_user,
            "session_id": self.session_id,
            "leak_mode": self.leak_mode,
            "leak_profile": self.leak_profile,
            "use_llm": self.use_llm,
        }
        url = f"{self.base_url}/chat"
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                raw = resp.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8")
            raise RuntimeError(f"HTTP target request failed: {exc.code} {body}") from exc

        data = json.loads(raw)
        reply = data.get("reply", "")
        server_audit = data.get("server_audit")
        return {
            "content": reply,
            "metadata": {"http_audit": server_audit},
        }


def _last_user_message(messages: List[Dict[str, str]]) -> str:
    for msg in reversed(messages):
        if msg.get("role") == "user":
            return msg.get("content", "")
    return ""
