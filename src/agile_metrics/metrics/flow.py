"""Métricas de fluxo core: cycle time, throughput, WIP."""

from __future__ import annotations

from datetime import timedelta

import pandas as pd

from agile_metrics.models import Board, Card


def _hours(td: timedelta) -> float:
    return td.total_seconds() / 3600


def cycle_time_hours(card: Card, start_column: str, done_column: str) -> float | None:
    start = card.entered(start_column)
    done = card.entered(done_column)
    if start is None or done is None or done < start:
        return None
    return _hours(done - start)


def completed_cards(board: Board) -> list[Card]:
    return [c for c in board.cards if c.entered(board.done_column) is not None]


def cycle_time_percentiles(
    board: Board, pcts: tuple[int, ...] = (50, 85, 95)
) -> dict[int, float]:
    """Percentis de cycle time em horas, sobre todos os cards concluídos."""
    values = [
        ct
        for c in completed_cards(board)
        if (ct := cycle_time_hours(c, board.start_column, board.done_column)) is not None
    ]
    if not values:
        return {p: float("nan") for p in pcts}
    series = pd.Series(values)
    return {p: float(series.quantile(p / 100)) for p in pcts}


def throughput_weekly(board: Board) -> pd.Series:
    """Quantidade de cards finalizados por semana ISO."""
    dates = [c.entered(board.done_column) for c in completed_cards(board)]
    if not dates:
        return pd.Series(dtype="int64")
    series = pd.Series(1, index=pd.DatetimeIndex(dates))
    return series.resample("W").sum()


def current_wip(board: Board) -> dict[str, int]:
    """Cards que estão agora em cada coluna que não é de conclusão."""
    counts = {c.name: 0 for c in board.columns}
    for card in board.cards:
        col = card.current_column()
        if col in counts:
            counts[col] += 1
    for name in board.done_column_names():
        counts.pop(name, None)
    return counts
