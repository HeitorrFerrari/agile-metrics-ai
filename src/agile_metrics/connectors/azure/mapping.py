"""Semântica do quadro fornecida pelo usuário (board_config.yaml) -> colunas normalizadas."""

from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import BaseModel

from agile_metrics.models import Column, ColumnType


class BoardConfig(BaseModel):
    name: str
    columns: list[Column]
    start_column: str
    done_column: str
    history_days: int = 90

    @classmethod
    def load(cls, path: str | Path) -> "BoardConfig":
        raw = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
        columns = [
            Column(
                name=c["name"],
                type=ColumnType(c["type"]),
                order=i,
                wip_limit=c.get("wip_limit"),
            )
            for i, c in enumerate(raw["columns"])
        ]
        return cls(
            name=raw["name"],
            columns=columns,
            start_column=raw["start_column"],
            done_column=raw["done_column"],
            history_days=raw.get("history_days", 90),
        )

    def column_for_state(self, state: str) -> Column | None:
        """Resolve um nome de coluna / state do Azure para uma coluna normalizada."""
        return next((c for c in self.columns if c.name == state), None)
