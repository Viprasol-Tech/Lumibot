import logging
from dataclasses import dataclass, field

logger = logging.getLogger("trading_bot.risk")


@dataclass
class RiskParams:
    risk_per_trade: float = 0.02
    max_positions: int = 5
    max_portfolio_risk: float = 0.06
    max_daily_loss: float = 0.03
    stop_loss_pct: float = 0.02
    take_profit_pct: float = 0.04
    use_trailing_stop: bool = False
    trailing_stop_pct: float = 0.015


class RiskManager:
    def __init__(self, params: RiskParams | None = None) -> None:
        self.params = params or RiskParams()
        self._daily_pnl: float = 0.0

    def can_open_position(self, current_positions: int, portfolio_value: float) -> bool:
        if current_positions >= self.params.max_positions:
            logger.warning("Max positions (%d) reached", self.params.max_positions)
            return False

        if self._daily_pnl <= -(self.params.max_daily_loss * portfolio_value):
            logger.warning("Max daily loss hit: $%.2f", self._daily_pnl)
            return False

        return True

    def calculate_stop_loss(self, entry_price: float, side: str) -> float:
        if side == "buy":
            return entry_price * (1 - self.params.stop_loss_pct)
        return entry_price * (1 + self.params.stop_loss_pct)

    def calculate_take_profit(self, entry_price: float, side: str) -> float:
        if side == "buy":
            return entry_price * (1 + self.params.take_profit_pct)
        return entry_price * (1 - self.params.take_profit_pct)

    def update_daily_pnl(self, pnl: float) -> None:
        self._daily_pnl += pnl
        logger.info("Daily P&L updated: $%.2f", self._daily_pnl)

    def reset_daily_pnl(self) -> None:
        self._daily_pnl = 0.0

    def is_kill_switch_triggered(self, portfolio_value: float, initial_value: float) -> bool:
        drawdown = (initial_value - portfolio_value) / initial_value
        if drawdown >= self.params.max_daily_loss:
            logger.critical("KILL SWITCH: Drawdown %.2f%% exceeds limit", drawdown * 100)
            return True
        return False
