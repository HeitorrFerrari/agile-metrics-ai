"""Rule definitions.

A rule reads the AnalysisContext and returns zero or more Findings. Keep every
claim backed by a number in `evidence` — the narrative layer is not allowed to
invent them.
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
                title="Active columns have no WIP limit",
                detail=(
                    "Limiting work in progress is Kanban's core mechanic. "
                    f"These active columns have no limit: {', '.join(missing)}."
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
                        title=f"WIP limit exceeded in '{col.name}'",
                        detail=f"{count} cards in the column vs a limit of {col.wip_limit}.",
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
        # TODO: read ctx.extras["aging_items"] produced by metrics.aging.aging_wip
        return []


class BackwardMovementRule:
    id = "backward-movement"

    def evaluate(self, ctx: AnalysisContext) -> list[Finding]:
        # TODO: count transitions where the destination column's order is lower
        #       than the source column's order (rework / failed hand-offs)
        return []


DEFAULT_RULES: list[Rule] = [
    NoWipLimitsRule(),
    WipLimitExceededRule(),
    AgingWipRule(),
    BackwardMovementRule(),
]
