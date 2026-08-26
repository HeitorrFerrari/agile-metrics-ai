from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from agile_metrics.models import Board, Card, Column, ColumnType, Transition

UTC = timezone.utc


def _card(cid: str, moves: list[tuple[str | None, str, datetime]]) -> Card:
    return Card(
        id=cid,
        title=f"Card {cid}",
        created_at=moves[0][2],
        transitions=[
            Transition(card_id=cid, from_column=src, to_column=dst, at=at)
            for src, dst, at in moves
        ],
    )


@pytest.fixture
def sample_board() -> Board:
    base = datetime(2026, 1, 1, tzinfo=UTC)
    cards = [
        _card(
            "1",
            [
                (None, "New", base),
                ("New", "Active", base + timedelta(days=1)),
                ("Active", "Closed", base + timedelta(days=4)),
            ],
        ),
        _card(
            "2",
            [
                (None, "New", base + timedelta(days=2)),
                ("New", "Active", base + timedelta(days=3)),
            ],
        ),
    ]
    return Board(
        name="Test Board",
        columns=[
            Column(name="New", type=ColumnType.QUEUE, order=0),
            Column(name="Active", type=ColumnType.ACTIVE, order=1, wip_limit=1),
            Column(name="Closed", type=ColumnType.DONE, order=2),
        ],
        cards=cards,
        start_column="Active",
        done_column="Closed",
    )
