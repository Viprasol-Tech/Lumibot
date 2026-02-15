import logging
from datetime import datetime, timezone

from bot.config import settings

logger = logging.getLogger("trading_bot")


def setup_logging() -> None:
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
        format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def utc_now() -> datetime:
    return datetime.now(timezone.utc)
