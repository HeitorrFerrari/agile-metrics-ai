"""Connector interface — turns a source tool's board into the normalized model."""

from __future__ import annotations

import abc
from datetime import datetime

from agile_metrics.models import Board


class Connector(abc.ABC):
    """Every provider (Azure DevOps, ClickUp, Jira, ...) implements this."""

    @abc.abstractmethod
    def fetch_board(self, since: datetime) -> Board:
        """Fetch the board plus each card's column-transition history since `since`."""
        raise NotImplementedError
