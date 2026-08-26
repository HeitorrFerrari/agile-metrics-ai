"""Thin wrapper over the Azure DevOps REST + Analytics APIs.

Auth: a personal access token (PAT) with at least `Work Items (Read)` and
`Analytics (Read)`. The PAT is sent as HTTP basic auth with an empty username.
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
        """Run a WIQL query, return the matching work item ids."""
        # TODO: POST /{project}/_apis/wit/wiql?api-version=REST_API_VERSION
        #       body: {"query": wiql}  -> response["workItems"][*]["id"]
        raise NotImplementedError

    def work_item_updates(self, work_item_id: int) -> list[dict[str, Any]]:
        """Field-level revision history for one work item (incl. state / column changes)."""
        # TODO: GET /{project}/_apis/wit/workItems/{id}/updates?api-version=REST_API_VERSION
        #       paginate on $top / $skip
        raise NotImplementedError

    def board_columns(self, board: str) -> list[dict[str, Any]]:
        """Board column definitions, including WIP limits."""
        # TODO: GET /{project}/{team}/_apis/work/boards/{board}/columns?api-version=REST_API_VERSION
        raise NotImplementedError

    # --- Analytics (OData, historical snapshots) -------------------------

    def board_snapshots(self, since_iso: str) -> list[dict[str, Any]]:
        """Daily WorkItemBoardSnapshot rows since `since_iso` — best source of history."""
        # TODO: GET /_odata/{ANALYTICS_API_VERSION}/WorkItemBoardSnapshot
        #       ?$filter=DateValue ge {since_iso}
        #       &$select=WorkItemId,DateValue,BoardColumn,State,ColumnPosition
        raise NotImplementedError

    def close(self) -> None:
        self._rest.close()
        self._analytics.close()
