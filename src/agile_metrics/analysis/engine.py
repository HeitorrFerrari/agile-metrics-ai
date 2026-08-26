from __future__ import annotations

from typing import Iterable

from pydantic import BaseModel, ConfigDict

from agile_metrics.analysis.findings import Finding
from agile_metrics.models import Board

_SEVERITY_ORDER = {"high": 0, "medium": 1, "low": 2, "info": 3}


class AnalysisContext(BaseModel):
    """Tudo que as regras precisam: o quadro mais as métricas pré-calculadas."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    board: Board
    cycle_time_pcts: dict[int, float]
    current_wip: dict[str, int]
    extras: dict = {}  # espaço para aging_items, cfd, littles_law, ... conforme as regras precisarem


def run_analysis(ctx: AnalysisContext, rules: Iterable) -> list[Finding]:
    findings: list[Finding] = []
    for rule in rules:
        findings.extend(rule.evaluate(ctx))
    return sorted(findings, key=lambda f: _SEVERITY_ORDER[f.severity.value])
