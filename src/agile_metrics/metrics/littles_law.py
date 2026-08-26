"""Sanity check da Lei de Little.

Para um sistema estável: cycle time médio ~= WIP médio / throughput.
Um desvio grande significa que o quadro não está em regime estável (a taxa de
chegada e a taxa de saída estão desbalanceadas).
"""

from __future__ import annotations

from pydantic import BaseModel


class LittlesLawResult(BaseModel):
    avg_wip: float
    weekly_throughput: float
    observed_cycle_time_days: float
    predicted_cycle_time_days: float
    deviation_ratio: float  # observado / previsto

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
