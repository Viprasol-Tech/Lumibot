"""Entry point for the trading bot."""

import sys
from pathlib import Path

# Ensure project root is on sys.path so both `bot` and local `lumibot` resolve.
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from lumibot.brokers import Alpaca
from lumibot.traders import Trader

from bot.config import settings
from bot.strategy import TradingStrategy
from bot.utils import setup_logging

setup_logging()


def main() -> None:
    broker = Alpaca(settings.alpaca_config)

    strategy = TradingStrategy(
        broker=broker,
        parameters={
            "symbol": "SPY",
            "risk_per_trade": 0.02,
            "max_positions": 5,
            "stop_loss_pct": 0.02,
            "take_profit_pct": 0.04,
        },
    )

    trader = Trader()
    trader.add_strategy(strategy)
    trader.run_all()


if __name__ == "__main__":
    main()
