import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")


class Settings:
    ALPACA_API_KEY: str = os.getenv("ALPACA_API_KEY", "")
    ALPACA_API_SECRET: str = os.getenv("ALPACA_API_SECRET", "")
    ALPACA_BASE_URL: str = os.getenv("ALPACA_BASE_URL", "https://paper-api.alpaca.markets")

    BOT_MODE: str = os.getenv("BOT_MODE", "paper")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/trading_bot")

    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    API_SECRET_KEY: str = os.getenv("API_SECRET_KEY", "change-me")

    @property
    def is_paper(self) -> bool:
        return self.BOT_MODE == "paper"

    @property
    def alpaca_config(self) -> dict:
        return {
            "API_KEY": self.ALPACA_API_KEY,
            "API_SECRET": self.ALPACA_API_SECRET,
            "PAPER": self.is_paper,
        }


settings = Settings()
