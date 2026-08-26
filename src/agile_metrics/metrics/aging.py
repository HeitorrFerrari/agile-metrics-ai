"""Aging WIP — cards that have sat in a column longer than they should."""

from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel

from agile_metrics.models import Board


class AgingItem(BaseModel):
    card_id: str
    title: str
    column: str
    age_hours: float
    threshold_hours: float


def aging_wip(
    board: Board, threshold_hours_by_column: dict[str, float]
) -> list[AgingItem]:
    """Cards older in their current column than the given threshold.

    A useful threshold is the overall cycle-time p85 (or a per-column budget).
    """
    now = datetime.now(timezone.utc)
    done = board.done_column_names()
    out: list[AgingItem] = []
    for card in board.cards:
        col = card.current_column()
        if col is None or col in done:
            continue
        age = card.time_in_column_hours(col, now=now)
        threshold = threshold_hours_by_column.get(col, float("inf"))
        if age > threshold:
            out.append(
                AgingItem(
                    card_id=card.id,
                    title=card.title,
                    column=col,
                    age_hours=age,
                    threshold_hours=threshold,
                )
            )
    return sorted(out, key=lambda a: a.age_hours, reverse=True)
