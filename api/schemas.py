from datetime import datetime

from pydantic import BaseModel


# ── Trades ──

class TradeOut(BaseModel):
    id: int
    symbol: str
    asset_type: str
    side: str
    order_type: str
    quantity: float
    price: float
    total_value: float
    pnl: float
    status: str
    filled_at: datetime | None
    created_at: datetime
    strike: float | None = None
    expiration: str | None = None
    option_type: str | None = None

    model_config = {"from_attributes": True}


# ── Positions ──

class PositionOut(BaseModel):
    id: int
    symbol: str
    asset_type: str
    side: str
    quantity: float
    entry_price: float
    current_price: float
    unrealized_pnl: float
    is_open: bool
    opened_at: datetime
    closed_at: datetime | None = None

    model_config = {"from_attributes": True}


# ── P&L ──

class PnlRecordOut(BaseModel):
    id: int
    date: datetime
    portfolio_value: float
    daily_pnl: float
    cumulative_pnl: float

    model_config = {"from_attributes": True}


# ── Bot Control ──

class BotStatus(BaseModel):
    status: str
    mode: str
    started_at: datetime | None = None

    model_config = {"from_attributes": True}


class BotCommand(BaseModel):
    action: str  # start, pause, stop


# ── Dashboard Overview ──

class DashboardOverview(BaseModel):
    account_value: float
    daily_pnl: float
    open_positions: int
    bot_status: str
    bot_mode: str


# ── Settings ──

class StrategySettings(BaseModel):
    symbol: str = "SPY"
    risk_per_trade: float = 0.02
    max_positions: int = 5
    stop_loss_pct: float = 0.02
    take_profit_pct: float = 0.04
    use_trailing_stop: bool = False
    trailing_stop_pct: float = 0.015
