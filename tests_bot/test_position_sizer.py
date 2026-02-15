import pytest
from bot.position_sizer import PositionSizer
from bot.risk_manager import RiskParams


@pytest.fixture
def sizer():
    return PositionSizer(RiskParams(risk_per_trade=0.02))


def test_calculate_shares_with_stop(sizer):
    shares = sizer.calculate_shares(
        portfolio_value=100_000,
        entry_price=50.0,
        stop_price=48.0,  # $2 risk per share
    )
    # risk = 100k * 0.02 = $2000, risk_per_share = $2 -> 1000 shares
    # but max 20% of portfolio = $20k / $50 = 400 shares
    assert shares == 400


def test_calculate_shares_without_stop(sizer):
    shares = sizer.calculate_shares(
        portfolio_value=100_000,
        entry_price=200.0,
    )
    # risk = $2000, shares = floor(2000/200) = 10
    assert shares == 10


def test_returns_zero_for_tiny_position(sizer):
    shares = sizer.calculate_shares(
        portfolio_value=100,
        entry_price=10_000.0,
    )
    assert shares == 0


def test_option_contracts(sizer):
    contracts = sizer.calculate_option_contracts(
        portfolio_value=100_000,
        premium=5.0,
        multiplier=100,
    )
    # risk = $2000, cost per contract = $500 -> 4 contracts
    assert contracts == 4
