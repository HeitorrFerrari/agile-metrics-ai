"""O modelo normalizado do quadro.

Todo conector mapeia a ferramenta de origem para estes tipos, então as camadas
de métricas e análise nunca tocam num payload específico de um provedor.

Todos os datetimes são timezone-aware em UTC.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, Field


def _now() -> datetime:
    return datetime.now(timezone.utc)


class ColumnType(str, Enum):
    QUEUE = "queue"    # esperando, ninguém trabalhando -> tempo de espera
    ACTIVE = "active"  # sendo trabalhado ativamente -> tempo de toque
    DONE = "done"      # saiu do sistema


class Column(BaseModel):
    name: str
    type: ColumnType
    order: int = 0
    wip_limit: int | None = None


class Transition(BaseModel):
    """Um único movimento de um card de uma coluna para outra."""

    card_id: str
    from_column: str | None
    to_column: str
    at: datetime


class Card(BaseModel):
    id: str
    title: str = ""
    card_type: str = ""  # ex.: "User Story", "Bug"
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
        """Primeira vez que o card entrou em `column`, ou None se nunca entrou."""
        for t in self.sorted_transitions():
            if t.to_column == column:
                return t.at
        return None

    def time_in_column_hours(self, column: str, now: datetime | None = None) -> float:
        """Total de horas passadas em `column` (aberto se o card ainda está lá)."""
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
