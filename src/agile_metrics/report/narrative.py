"""Ask Claude to turn deterministic findings into a prioritized coaching summary."""

from __future__ import annotations

import json

from agile_metrics.analysis.findings import Finding
from agile_metrics.llm.client import LLMClient

SYSTEM = (
    "You are an agile delivery coach. You are given deterministic findings about "
    "a team's Kanban board. Explain what they mean for flow, rank the three "
    "highest-impact problems, and give concrete, specific actions the team can "
    "take. Never invent metrics or numbers that are not in the findings."
)


def generate_narrative(findings: list[Finding], llm: LLMClient) -> str:
    payload = [f.model_dump(mode="json") for f in findings]
    prompt = (
        "Findings (JSON):\n"
        f"{json.dumps(payload, indent=2, ensure_ascii=False)}\n\n"
        "Write the coaching summary in Brazilian Portuguese (pt-BR)."
    )
    return llm.complete(SYSTEM, prompt)
