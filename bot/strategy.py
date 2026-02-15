import logging
from datetime import datetime

from lumibot.strategies.strategy import Strategy

from bot.risk_manager import RiskManager, RiskParams
from bot.position_sizer import PositionSizer

logger = logging.getLogger("trading_bot.strategy")


class TradingStrategy(Strategy):
    """Main strategy class — override on_trading_iteration with converted thinkScript logic.

    This is a scaffold. When the client provides their thinkScript strategy,
    the entry/exit conditions will be implemented inside on_trading_iteration().
    """

    parameters = {
        "symbol": "SPY",
        "risk_per_trade": 0.02,
        "max_positions": 5,
        "stop_loss_pct": 0.02,
        "take_profit_pct": 0.04,
        "use_trailing_stop": False,
        "trailing_stop_pct": 0.015,
    }

    def initialize(self) -> None:
        self.sleeptime = "1M"  # Run every 1 minute

        risk_params = RiskParams(
            risk_per_trade=self.parameters["risk_per_trade"],
            max_positions=self.parameters["max_positions"],
            stop_loss_pct=self.parameters["stop_loss_pct"],
            take_profit_pct=self.parameters["take_profit_pct"],
            use_trailing_stop=self.parameters["use_trailing_stop"],
            trailing_stop_pct=self.parameters["trailing_stop_pct"],
        )
        self.risk_manager = RiskManager(risk_params)
        self.position_sizer = PositionSizer(risk_params)
        self._initial_value: float | None = None

        logger.info("Strategy initialized — symbol=%s, mode=%s", self.parameters["symbol"], "PAPER" if self.broker._is_paper else "LIVE")

    def on_trading_iteration(self) -> None:
        symbol = self.parameters["symbol"]
        portfolio_value = self.get_portfolio_value()

        if self._initial_value is None:
            self._initial_value = portfolio_value

        # Kill switch check
        if self.risk_manager.is_kill_switch_triggered(portfolio_value, self._initial_value):
            logger.critical("Kill switch triggered — selling all positions")
            self.sell_all()
            return

        current_positions = len(self.get_positions())

        # ── PLACEHOLDER: thinkScript signal logic goes here ──
        # When the client provides thinkScript, convert indicators and
        # entry/exit conditions into this method.
        #
        # Example skeleton:
        #
        #   bars = self.get_historical_prices(symbol, 50, "day")
        #   df = bars.df
        #   # Compute indicators (SMA, RSI, MACD, etc.)
        #   # Generate buy/sell signals
        #   # Check risk rules
        #   # Submit orders
        #
        logger.debug("Trading iteration — portfolio=$%.2f, positions=%d", portfolio_value, current_positions)

    def before_market_opens(self) -> None:
        self.risk_manager.reset_daily_pnl()
        logger.info("Pre-market: daily P&L reset")

    def after_market_closes(self) -> None:
        portfolio_value = self.get_portfolio_value()
        logger.info("Post-market: portfolio=$%.2f", portfolio_value)

    def on_filled_order(self, position, order, price, quantity, multiplier) -> None:
        side = order.side
        symbol = order.asset.symbol if hasattr(order.asset, "symbol") else str(order.asset)
        logger.info(
            "Order filled: %s %s x%d @ $%.2f (mult=%s)",
            side, symbol, quantity, price, multiplier,
        )
        # TODO: log to PostgreSQL via the API
