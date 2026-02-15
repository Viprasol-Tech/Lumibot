import pytest
from bot.risk_manager import RiskManager, RiskParams


@pytest.fixture
def rm():
    return RiskManager(RiskParams(max_positions=3, max_daily_loss=0.03))


def test_can_open_position_within_limits(rm):
    assert rm.can_open_position(current_positions=2, portfolio_value=100_000) is True


def test_cannot_exceed_max_positions(rm):
    assert rm.can_open_position(current_positions=3, portfolio_value=100_000) is False


def test_daily_loss_blocks_trades(rm):
    rm.update_daily_pnl(-3100)  # exceeds 3% of 100k
    assert rm.can_open_position(current_positions=0, portfolio_value=100_000) is False


def test_stop_loss_calculation():
    rm = RiskManager(RiskParams(stop_loss_pct=0.02))
    assert rm.calculate_stop_loss(100.0, "buy") == pytest.approx(98.0)
    assert rm.calculate_stop_loss(100.0, "sell") == pytest.approx(102.0)


def test_kill_switch():
    rm = RiskManager(RiskParams(max_daily_loss=0.05))
    assert rm.is_kill_switch_triggered(95_000, 100_000) is True
    assert rm.is_kill_switch_triggered(96_000, 100_000) is False


def test_reset_daily_pnl(rm):
    rm.update_daily_pnl(-1000)
    rm.reset_daily_pnl()
    assert rm.can_open_position(current_positions=0, portfolio_value=100_000) is True
