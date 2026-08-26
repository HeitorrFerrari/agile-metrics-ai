"""Cumulative Flow Diagram data."""

from __future__ import annotations

import pandas as pd

from agile_metrics.models import Board


def cumulative_flow(board: Board, freq: str = "D") -> pd.DataFrame:
    """Build a cumulative flow table.

    index  = date (at `freq` resolution)
    column = board column
    value  = number of cards in that column or a later one on that date

    Derived by replaying every card's transitions onto a timeline.
    Widening bands = growing WIP / a bottleneck downstream.
    """
    # TODO: replay transitions per card, forward-fill state per day,
    #       pivot to a date x column matrix, then cumulate from the right.
    raise NotImplementedError
