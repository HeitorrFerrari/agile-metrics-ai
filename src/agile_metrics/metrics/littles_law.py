"""Little's Law sanity check.

For a stable system: average cycle time ~= average WIP / throughput.
A large deviation means the board is not in a steady state (arrival rate and
departure rate are out of balance).
"""

from __future__ import annotations

from pydantic import BaseModel


class LittlesLawResult(BaseModel):
    avg_wip: float
    weekly_throughput: float
    observed_cycle_time_days: float
    predicted_cycle_time_days: float
    deviation_ratio: float  # observed / predicted

    @property
    def stable(self) -> bool:
        return 0.75 <= self.deviation_ratio <= 1.33


def littles_law_check(
    avg_wip: float, weekly_throughput: float, observed_cycle_time_days: float
) -> LittlesLawResult:
    daily_tp = weekly_throughput / 7 if weekly_throughput else float("nan")
    predicted = avg_wip / daily_tp if daily_tp else float("nan")
    ratio = observed_cycle_time_days / predicted if predicted else float("nan")
    return LittlesLawResult(
        avg_wip=avg_wip,
        weekly_throughput=weekly_throughput,
        observed_cycle_time_days=observed_cycle_time_days,
        predicted_cycle_time_days=predicted,
        deviation_ratio=ratio,
    )
