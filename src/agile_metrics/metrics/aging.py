"""Aging WIP — cards parados numa coluna por mais tempo do que deveriam."""

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
    """Cards mais velhos na coluna atual do que o limiar informado.

    Um limiar útil é o p85 geral do cycle time (ou um orçamento por coluna).
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
