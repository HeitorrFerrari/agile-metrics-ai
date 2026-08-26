"""Azure DevOps -> normalized Board."""

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
        MVP plan:
          1. WIQL: work items on the board changed since `since`, plus everything
             still open.
          2. For each work item: work_item_updates() -> read System.BoardColumn /
             System.State changes -> build list[Transition].
          3. Cross-check / backfill with board_snapshots() for history the updates
             feed does not cover reliably.
          4. Map every state name to a normalized Column via self.config.
          5. Build Board(columns=self.config.columns, cards=[...], ...).
        """
        # TODO: implement the steps above.
        raise NotImplementedError
