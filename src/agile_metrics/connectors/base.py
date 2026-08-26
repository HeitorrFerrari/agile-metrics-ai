"""Interface do conector — transforma o quadro da ferramenta de origem no modelo normalizado."""

from __future__ import annotations

import abc
from datetime import datetime

from agile_metrics.models import Board


class Connector(abc.ABC):
    """Todo provedor (Azure DevOps, ClickUp, Jira, ...) implementa isto."""

    @abc.abstractmethod
    def fetch_board(self, since: datetime) -> Board:
        """Busca o quadro e o histórico de transição de coluna de cada card desde `since`."""
        raise NotImplementedError
