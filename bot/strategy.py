import logging

import pandas_ta as ta
from lumibot.strategies.strategy import Strategy

from bot.risk_manager import RiskManager, RiskParams
from bot.position_sizer import PositionSizer

logger = logging.getLogger("trading_bot.strategy")


class TradingStrategy(Strategy):
    """SMA crossover + RSI filter strategy.

    Entry (BUY):
      - SMA fast crosses above SMA slow  (golden cross)
      - RSI is below overbought threshold (< 70)
      - No existing position in the symbol

    Exit (SELL):
      - SMA fast crosses below SMA slow  (death cross)
      - OR RSI rises above overbought threshold (> 80)
      - OR stop-loss / take-profit hit

    When the client provides their thinkScript code, replace the indicator
    calculations and signal logic inside on_trading_iteration().
    """

    parameters = {
        "symbol": "SPY",
        "sma_fast": 9,
        "sma_slow": 21,
        "rsi_period": 14,
        "rsi_overbought": 70,
        "rsi_exit": 80,
        "rsi_oversold": 30,
        "risk_per_trade": 0.02,
        "max_positions": 5,
        "stop_loss_pct": 0.02,
        "take_profit_pct": 0.04,
        "use_trailing_stop": False,
        "trailing_stop_pct": 0.015,
    }

    # ──────────────────── Lifecycle ────────────────────

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
        self._entry_prices: dict[str, float] = {}

        logger.info(
            "Strategy initialized — symbol=%s, SMA(%d/%d), RSI(%d)",
            self.parameters["symbol"],
            self.parameters["sma_fast"],
            self.parameters["sma_slow"],
            self.parameters["rsi_period"],
        )

    def before_market_opens(self) -> None:
        self.risk_manager.reset_daily_pnl()
        logger.info("Pre-market: daily P&L reset")

    def after_market_closes(self) -> None:
        portfolio_value = self.get_portfolio_value()
        logger.info("Post-market: portfolio=$%.2f", portfolio_value)

    # ──────────────────── Main Loop ────────────────────

    def on_trading_iteration(self) -> None:
        symbol = self.parameters["symbol"]
        portfolio_value = self.get_portfolio_value()

        if self._initial_value is None:
            self._initial_value = portfolio_value

        # Kill switch
        if self.risk_manager.is_kill_switch_triggered(portfolio_value, self._initial_value):
            logger.critical("KILL SWITCH — selling all positions")
            self.sell_all()
            return

        # Fetch historical data — need enough bars for the slow SMA + buffer
        lookback = self.parameters["sma_slow"] + 10
        bars = self.get_historical_prices(symbol, lookback, "minute")
        if bars is None or bars.df is None or len(bars.df) < self.parameters["sma_slow"]:
            logger.warning("Not enough data for %s (%s bars)", symbol, 0 if bars is None else len(bars.df))
            return

        df = bars.df

        # ── Compute indicators ──
        df["sma_fast"] = ta.sma(df["close"], length=self.parameters["sma_fast"])
        df["sma_slow"] = ta.sma(df["close"], length=self.parameters["sma_slow"])
        df["rsi"] = ta.rsi(df["close"], length=self.parameters["rsi_period"])

        # Drop rows where indicators haven't warmed up yet
        df = df.dropna(subset=["sma_fast", "sma_slow", "rsi"])
        if len(df) < 2:
            return

        # Current and previous values
        curr = df.iloc[-1]
        prev = df.iloc[-2]
        price = float(curr["close"])
        rsi = float(curr["rsi"])
        sma_fast_now = float(curr["sma_fast"])
        sma_slow_now = float(curr["sma_slow"])
        sma_fast_prev = float(prev["sma_fast"])
        sma_slow_prev = float(prev["sma_slow"])

        position = self.get_position(symbol)
        current_positions = len(self.get_positions())

        logger.info(
            "%s | price=$%.2f | SMA(%d)=%.2f SMA(%d)=%.2f | RSI=%.1f | pos=%s",
            symbol, price,
            self.parameters["sma_fast"], sma_fast_now,
            self.parameters["sma_slow"], sma_slow_now,
            rsi,
            f"{position.quantity}" if position else "none",
        )

        # ── EXIT signals ──
        if position and position.quantity > 0:
            entry_price = self._entry_prices.get(symbol, price)

            # Death cross: fast SMA crosses below slow SMA
            death_cross = sma_fast_prev >= sma_slow_prev and sma_fast_now < sma_slow_now

            # RSI extreme overbought
            rsi_exit = rsi > self.parameters["rsi_exit"]

            # Stop-loss
            stop_price = self.risk_manager.calculate_stop_loss(entry_price, "buy")
            stop_hit = price <= stop_price

            # Take-profit
            tp_price = self.risk_manager.calculate_take_profit(entry_price, "buy")
            tp_hit = price >= tp_price

            if death_cross or rsi_exit or stop_hit or tp_hit:
                reason = (
                    "death cross" if death_cross else
                    "RSI overbought" if rsi_exit else
                    "stop-loss" if stop_hit else
                    "take-profit"
                )
                logger.info("SELL signal [%s] — closing %s position", reason, symbol)
                order = self.create_order(symbol, position.quantity, "sell")
                self.submit_order(order)
                self._entry_prices.pop(symbol, None)
                return

        # ── ENTRY signals ──
        if position is None or position.quantity == 0:
            # Golden cross: fast SMA crosses above slow SMA
            golden_cross = sma_fast_prev <= sma_slow_prev and sma_fast_now > sma_slow_now

            # RSI not overbought
            rsi_ok = rsi < self.parameters["rsi_overbought"]

            if golden_cross and rsi_ok:
                if not self.risk_manager.can_open_position(current_positions, portfolio_value):
                    logger.warning("Risk manager blocked new position")
                    return

                stop_price = self.risk_manager.calculate_stop_loss(price, "buy")
                shares = self.position_sizer.calculate_shares(portfolio_value, price, stop_price)
                if shares <= 0:
                    return

                logger.info("BUY signal — %d shares of %s @ $%.2f", shares, symbol, price)
                order = self.create_order(symbol, shares, "buy")
                self.submit_order(order)
                self._entry_prices[symbol] = price

    # ──────────────────── Callbacks ────────────────────

    def on_filled_order(self, position, order, price, quantity, multiplier) -> None:
        side = order.side
        symbol = order.asset.symbol if hasattr(order.asset, "symbol") else str(order.asset)
        logger.info(
            "ORDER FILLED: %s %s x%d @ $%.2f (mult=%s)",
            side, symbol, quantity, price, multiplier,
        )

        if side == "sell":
            entry = self._entry_prices.get(symbol, price)
            pnl = (price - entry) * quantity
            self.risk_manager.update_daily_pnl(pnl)
            logger.info("Trade P&L: $%.2f (entry=$%.2f, exit=$%.2f)", pnl, entry, price)
