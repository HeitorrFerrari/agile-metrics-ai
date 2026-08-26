"""The normalized board model.

Every connector maps its source tool onto these types, so the metrics and
analysis layers never touch a provider-specific payload.

All datetimes are timezone-aware UTC.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, Field


def _now() -> datetime:
    return datetime.now(timezone.utc)


class ColumnType(str, Enum):
    QUEUE = "queue"    # waiting, nobody working it -> wait time
    ACTIVE = "active"  # actively being worked -> touch time
    DONE = "done"      # left the system


class Column(BaseModel):
    name: str
    type: ColumnType
    order: int = 0
    wip_limit: int | None = None


class Transition(BaseModel):
    """A single move of a card from one column to another."""

    card_id: str
    from_column: str | None
    to_column: str
    at: datetime


class Card(BaseModel):
    id: str
    title: str = ""
    card_type: str = ""  # e.g. "User Story", "Bug"
    created_at: datetime
    closed_at: datetime | None = None
    blocked: bool = False
    transitions: list[Transition] = Field(default_factory=list)

    def sorted_transitions(self) -> list[Transition]:
        return sorted(self.transitions, key=lambda t: t.at)

    def current_column(self) -> str | None:
        ts = self.sorted_transitions()
        return ts[-1].to_column if ts else None

    def entered(self, column: str) -> datetime | None:
        """First time the card entered `column`, or None if it never did."""
        for t in self.sorted_transitions():
            if t.to_column == column:
                return t.at
        return None

    def time_in_column_hours(self, column: str, now: datetime | None = None) -> float:
        """Total hours spent in `column` (open-ended if the card is still there)."""
        now = now or _now()
        total = 0.0
        entered_at: datetime | None = None
        for t in self.sorted_transitions():
            if t.to_column == column and entered_at is None:
                entered_at = t.at
            elif t.from_column == column and entered_at is not None:
                total += (t.at - entered_at).total_seconds() / 3600
                entered_at = None
        if entered_at is not None:
            total += (now - entered_at).total_seconds() / 3600
        return total


class Board(BaseModel):
    name: str
    columns: list[Column]
    cards: list[Card] = Field(default_factory=list)
    start_column: str
    done_column: str
    fetched_at: datetime = Field(default_factory=_now)

    def column(self, name: str) -> Column | None:
        return next((c for c in self.columns if c.name == name), None)

    def done_column_names(self) -> set[str]:
        return {c.name for c in self.columns if c.type is ColumnType.DONE}

    def active_cards(self) -> list[Card]:
        done = self.done_column_names()
        return [c for c in self.cards if c.current_column() not in done]
