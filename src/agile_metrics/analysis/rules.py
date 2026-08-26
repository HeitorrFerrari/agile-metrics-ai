"""Definições das regras.

Uma regra lê o AnalysisContext e retorna zero ou mais Findings. Mantenha toda
afirmação sustentada por um número em `evidence` — a camada de narrativa não
tem permissão para inventar números.
"""

from __future__ import annotations

from typing import Protocol

from agile_metrics.analysis.engine import AnalysisContext
from agile_metrics.analysis.findings import Finding, Severity
from agile_metrics.models import ColumnType


class Rule(Protocol):
    id: str

    def evaluate(self, ctx: AnalysisContext) -> list[Finding]: ...


class NoWipLimitsRule:
    id = "no-wip-limits"

    def evaluate(self, ctx: AnalysisContext) -> list[Finding]:
        active = [c for c in ctx.board.columns if c.type is ColumnType.ACTIVE]
        missing = [c.name for c in active if c.wip_limit is None]
        if not missing:
            return []
        return [
            Finding(
                rule_id=self.id,
                severity=Severity.HIGH,
                title="Colunas ativas sem limite de WIP",
                detail=(
                    "Limitar o trabalho em progresso é o mecanismo central do Kanban. "
                    f"Estas colunas ativas não têm limite: {', '.join(missing)}."
                ),
                evidence={"columns": missing},
            )
        ]


class WipLimitExceededRule:
    id = "wip-limit-exceeded"

    def evaluate(self, ctx: AnalysisContext) -> list[Finding]:
        out: list[Finding] = []
        for col in ctx.board.columns:
            if col.wip_limit is None:
                continue
            count = ctx.current_wip.get(col.name, 0)
            if count > col.wip_limit:
                out.append(
                    Finding(
                        rule_id=self.id,
                        severity=Severity.MEDIUM,
                        title=f"Limite de WIP estourado em '{col.name}'",
                        detail=f"{count} cards na coluna contra um limite de {col.wip_limit}.",
                        evidence={
                            "column": col.name,
                            "count": count,
                            "limit": col.wip_limit,
                        },
                    )
                )
        return out


class AgingWipRule:
    id = "aging-wip"

    def evaluate(self, ctx: AnalysisContext) -> list[Finding]:
        # TODO: ler ctx.extras["aging_items"] produzido por metrics.aging.aging_wip
        return []


class BackwardMovementRule:
    id = "backward-movement"

    def evaluate(self, ctx: AnalysisContext) -> list[Finding]:
        # TODO: contar transições em que a `order` da coluna de destino é menor
        #       que a da coluna de origem (retrabalho / hand-offs que falharam)
        return []


DEFAULT_RULES: list[Rule] = [
    NoWipLimitsRule(),
    WipLimitExceededRule(),
    AgingWipRule(),
    BackwardMovementRule(),
]
