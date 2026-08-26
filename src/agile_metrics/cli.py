"""Command-line entry point."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import typer
from rich import print as rprint

from agile_metrics.analysis.engine import AnalysisContext, run_analysis
from agile_metrics.analysis.rules import DEFAULT_RULES
from agile_metrics.config import load_settings
from agile_metrics.connectors.azure.client import AzureDevOpsClient
from agile_metrics.connectors.azure.connector import AzureConnector
from agile_metrics.connectors.azure.mapping import BoardConfig
from agile_metrics.metrics import flow
from agile_metrics.report.render import render_markdown

app = typer.Typer(help="Analyze an agile board and assess Kanban health.")


@app.command()
def analyze(narrative: bool = typer.Option(False, help="Add an LLM coaching summary.")) -> None:
    """Fetch the board, compute metrics, run the rules, print a report."""
    settings = load_settings()
    config = BoardConfig.load(settings.board_config_path)

    client = AzureDevOpsClient(
        org=settings.azure_devops_org,
        project=settings.azure_devops_project,
        pat=settings.azure_devops_pat,
        team=settings.azure_devops_team or None,
    )
    connector = AzureConnector(client, config)
    since = datetime.now(timezone.utc) - timedelta(days=config.history_days)
    board = connector.fetch_board(since)

    ctx = AnalysisContext(
        board=board,
        cycle_time_pcts=flow.cycle_time_percentiles(board),
        current_wip=flow.current_wip(board),
    )
    findings = run_analysis(ctx, DEFAULT_RULES)

    summary = None
    if narrative:
        from agile_metrics.llm.client import LLMClient
        from agile_metrics.report.narrative import generate_narrative

        summary = generate_narrative(
            findings, LLMClient(settings.anthropic_api_key, settings.anthropic_model)
        )

    rprint(render_markdown(board.name, ctx.cycle_time_pcts, ctx.current_wip, findings, summary))


@app.command()
def snapshot() -> None:
    """Save today's board state to data/snapshots/ to build history over time."""
    raise typer.Exit("TODO: implement daily snapshot capture")


if __name__ == "__main__":
    app()
