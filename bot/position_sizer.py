import logging
import math

from bot.risk_manager import RiskParams

logger = logging.getLogger("trading_bot.sizer")


class PositionSizer:
    def __init__(self, params: RiskParams | None = None) -> None:
        self.params = params or RiskParams()

    def calculate_shares(
        self,
        portfolio_value: float,
        entry_price: float,
        stop_price: float | None = None,
    ) -> int:
        risk_amount = portfolio_value * self.params.risk_per_trade

        if stop_price and entry_price != stop_price:
            risk_per_share = abs(entry_price - stop_price)
            shares = math.floor(risk_amount / risk_per_share)
        else:
            shares = math.floor(risk_amount / entry_price)

        if shares < 1:
            logger.warning("Position size < 1 share, skipping trade")
            return 0

        max_position_value = portfolio_value * 0.20
        max_shares = math.floor(max_position_value / entry_price)
        shares = min(shares, max_shares)

        logger.info(
            "Position size: %d shares @ $%.2f (risk $%.2f)",
            shares, entry_price, risk_amount,
        )
        return shares

    def calculate_option_contracts(
        self,
        portfolio_value: float,
        premium: float,
        multiplier: int = 100,
    ) -> int:
        risk_amount = portfolio_value * self.params.risk_per_trade
        cost_per_contract = premium * multiplier
        if cost_per_contract <= 0:
            return 0
        contracts = math.floor(risk_amount / cost_per_contract)
        return max(contracts, 0)
