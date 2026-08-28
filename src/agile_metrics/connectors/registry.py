from __future__ import annotations

from enum import Enum
from typing import Callable

from agile_metrics.config import Settings
from agile_metrics.connectors.azure.mapping import BoardConfig
from agile_metrics.connectors.base import Connector

class Provider(str, Enum):
    AZURE = "azure"
    JIRA = "jira"
    CLICKUP = "click-up"
    TRELLO = "trello"

ConnectorBuilder = Callable[[Settings, BoardConfig], Connector]
_BUILDERS: dict[Provider, ConnectorBuilder] = {}

def register(provider: Provider) -> Callable[[ConnectorBuilder], Connector]:
    def deco(fn: ConnectorBuilder) -> ConnectorBuilder:
        _BUILDERS[provider] = fn
        return fn
    return deco

def build_connector(provider: Provider, settings: Settings, config: BoardConfig) -> Connector:
    if provider not in _BUILDERS:
        raise ValueError(f"Sem conector registrado pro provider: {provider}")
    return _BUILDERS[provider](settings, config)