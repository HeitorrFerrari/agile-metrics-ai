"""Dados do Cumulative Flow Diagram (CFD)."""

from __future__ import annotations

import pandas as pd

from agile_metrics.models import Board


def cumulative_flow(board: Board, freq: str = "D") -> pd.DataFrame:
    """Monta a tabela de fluxo cumulativo.

    índice = data (na resolução de `freq`)
    coluna = coluna do quadro
    valor  = número de cards naquela coluna ou numa posterior naquela data

    Derivado reproduzindo as transições de cada card numa linha do tempo.
    Faixas alargando = WIP crescendo / gargalo mais adiante.
    """
    # TODO: reproduzir as transições por card, forward-fill do estado por dia,
    #       pivotar para uma matriz data x coluna e acumular da direita p/ esquerda.
    raise NotImplementedError
