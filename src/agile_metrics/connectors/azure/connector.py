"""Azure DevOps -> Board normalizado."""

from __future__ import annotations

from datetime import datetime

from agile_metrics.connectors.azure.client import AzureDevOpsClient
from agile_metrics.connectors.azure.mapping import BoardConfig
from agile_metrics.connectors.base import Connector
from agile_metrics.models import Board


class AzureConnector(Connector):
    def __init__(self, client: AzureDevOpsClient, config: BoardConfig) -> None:
        self.client = client
        self.config = config

    def fetch_board(self, since: datetime) -> Board:
        """
        Plano do MVP:
          1. WIQL: work items do quadro alterados desde `since`, mais tudo que
             ainda está aberto.
          2. Para cada work item: work_item_updates() -> ler mudanças de
             System.BoardColumn / System.State -> montar list[Transition].
          3. Cruzar / preencher com board_snapshots() para o histórico que o
             feed de updates não cobre de forma confiável.
          4. Mapear cada nome de state para uma Column normalizada via self.config.
          5. Montar Board(columns=self.config.columns, cards=[...], ...).
        """
        # TODO: implementar os passos acima.
        raise NotImplementedError
