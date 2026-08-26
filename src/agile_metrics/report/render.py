"""Renderiza métricas + findings como markdown."""

from __future__ import annotations

import math

from agile_metrics.analysis.findings import Finding


def _days(hours: float) -> str:
    return "n/a" if math.isnan(hours) else f"{hours / 24:.1f} d"


def render_markdown(
    board_name: str,
    cycle_time_pcts: dict[int, float],
    wip: dict[str, int],
    findings: list[Finding],
    narrative: str | None = None,
) -> str:
    lines = [f"# Saúde do Kanban - {board_name}", ""]

    lines.append("## Métricas de fluxo")
    for pct, value in cycle_time_pcts.items():
        lines.append(f"- Cycle time p{pct}: {_days(value)}")
    lines.append("")

    lines.append("## WIP atual")
    for column, count in wip.items():
        lines.append(f"- {column}: {count}")
    lines.append("")

    lines.append("## Findings")
    if not findings:
        lines.append("- nenhum")
    for f in findings:
        lines.append(f"- **[{f.severity.value.upper()}] {f.title}** - {f.detail}")

    if narrative:
        lines += ["", "## Resumo de coaching", "", narrative]

    return "\n".join(lines)
