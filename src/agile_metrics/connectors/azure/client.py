"""Wrapper fino sobre as APIs REST + Analytics do Azure DevOps.

Auth: um personal access token (PAT) com pelo menos `Work Items (Read)` e
`Analytics (Read)`. O PAT é enviado como HTTP basic auth com usuário vazio.
"""

from __future__ import annotations

import base64
from typing import Any

import httpx

REST_API_VERSION = "7.1"
ANALYTICS_API_VERSION = "v4.0-preview"


class AzureDevOpsClient:
    def __init__(
        self, org: str, project: str, pat: str, team: str | None = None
    ) -> None:
        self.org = org
        self.project = project
        self.team = team
        token = base64.b64encode(f":{pat}".encode()).decode()
        auth = {"Authorization": f"Basic {token}"}
        self._rest = httpx.Client(
            base_url=f"https://dev.azure.com/{org}",
            headers=auth,
            timeout=30.0,
        )
        self._analytics = httpx.Client(
            base_url=f"https://analytics.dev.azure.com/{org}/{project}",
            headers=auth,
            timeout=60.0,
        )

    # --- REST -------------------------------------------------------------

    def query_wiql(self, wiql: str) -> list[int]:
        """Roda uma consulta WIQL e retorna os ids dos work items correspondentes."""
        # TODO: POST /{project}/_apis/wit/wiql?api-version=REST_API_VERSION
        #       body: {"query": wiql}  -> response["workItems"][*]["id"]
        raise NotImplementedError

    def work_item_updates(self, work_item_id: int) -> list[dict[str, Any]]:
        """Histórico de revisões de um work item (inclui mudanças de state / coluna)."""
        # TODO: GET /{project}/_apis/wit/workItems/{id}/updates?api-version=REST_API_VERSION
        #       paginar com $top / $skip
        raise NotImplementedError

    def board_columns(self, board: str) -> list[dict[str, Any]]:
        """Definições das colunas do quadro, incluindo os limites de WIP."""
        # TODO: GET /{project}/{team}/_apis/work/boards/{board}/columns?api-version=REST_API_VERSION
        raise NotImplementedError

    # --- Analytics (OData, snapshots históricos) -------------------------

    def board_snapshots(self, since_iso: str) -> list[dict[str, Any]]:
        """Linhas diárias de WorkItemBoardSnapshot desde `since_iso` — melhor fonte de histórico."""
        # TODO: GET /_odata/{ANALYTICS_API_VERSION}/WorkItemBoardSnapshot
        #       ?$filter=DateValue ge {since_iso}
        #       &$select=WorkItemId,DateValue,BoardColumn,State,ColumnPosition
        raise NotImplementedError

    def close(self) -> None:
        self._rest.close()
        self._analytics.close()
