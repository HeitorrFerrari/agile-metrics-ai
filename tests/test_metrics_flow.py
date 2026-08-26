from agile_metrics.analysis.engine import AnalysisContext
from agile_metrics.analysis.rules import NoWipLimitsRule, WipLimitExceededRule
from agile_metrics.metrics import flow
from agile_metrics.models import Board


def test_cycle_time_percentiles(sample_board: Board) -> None:
    pcts = flow.cycle_time_percentiles(sample_board, pcts=(50,))
    assert pcts[50] == 72.0  # card 1: Active -> Closed = 3 dias


def test_current_wip(sample_board: Board) -> None:
    assert flow.current_wip(sample_board) == {"New": 0, "Active": 1}


def test_wip_limit_not_exceeded(sample_board: Board) -> None:
    ctx = AnalysisContext(
        board=sample_board,
        cycle_time_pcts={},
        current_wip=flow.current_wip(sample_board),
    )
    assert WipLimitExceededRule().evaluate(ctx) == []


def test_no_wip_limits_flags_missing(sample_board: Board) -> None:
    # "Active" tem limite, então nenhum finding é esperado aqui.
    ctx = AnalysisContext(
        board=sample_board, cycle_time_pcts={}, current_wip=flow.current_wip(sample_board)
    )
    assert NoWipLimitsRule().evaluate(ctx) == []
