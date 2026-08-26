"""Pede ao Claude para transformar findings determinísticos num resumo de coaching priorizado."""

from __future__ import annotations

import json

from agile_metrics.analysis.findings import Finding
from agile_metrics.llm.client import LLMClient

SYSTEM = (
    "Você é um coach de entrega ágil. Você recebe findings determinísticos sobre "
    "o quadro Kanban de um time. Explique o que eles significam para o fluxo, "
    "ranqueie os três problemas de maior impacto e dê ações concretas e "
    "específicas que o time pode tomar. Nunca invente métricas ou números que "
    "não estejam nos findings."
)


def generate_narrative(findings: list[Finding], llm: LLMClient) -> str:
    payload = [f.model_dump(mode="json") for f in findings]
    prompt = (
        "Findings (JSON):\n"
        f"{json.dumps(payload, indent=2, ensure_ascii=False)}\n\n"
        "Escreva o resumo de coaching em português do Brasil (pt-BR)."
    )
    return llm.complete(SYSTEM, prompt)
