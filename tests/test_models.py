from agile_metrics.models import Board


def test_current_column(sample_board: Board) -> None:
    by_id = {c.id: c for c in sample_board.cards}
    assert by_id["1"].current_column() == "Closed"
    assert by_id["2"].current_column() == "Active"


def test_time_in_column_hours(sample_board: Board) -> None:
    card = next(c for c in sample_board.cards if c.id == "1")
    assert round(card.time_in_column_hours("Active")) == 72  # 3 dias
