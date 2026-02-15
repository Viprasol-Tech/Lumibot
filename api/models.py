from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, Enum as SAEnum
from sqlalchemy.sql import func

from api.database import Base


class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), nullable=False, index=True)
    asset_type = Column(String(10), default="stock")  # stock, option
    side = Column(String(10), nullable=False)  # buy, sell
    order_type = Column(String(20), default="market")
    quantity = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    total_value = Column(Float, nullable=False)
    pnl = Column(Float, default=0.0)
    status = Column(String(20), default="filled")
    filled_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Option-specific fields
    strike = Column(Float, nullable=True)
    expiration = Column(String(20), nullable=True)
    option_type = Column(String(4), nullable=True)  # call, put


class Position(Base):
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), nullable=False, index=True)
    asset_type = Column(String(10), default="stock")
    side = Column(String(10), default="long")
    quantity = Column(Float, nullable=False)
    entry_price = Column(Float, nullable=False)
    current_price = Column(Float, default=0.0)
    unrealized_pnl = Column(Float, default=0.0)
    is_open = Column(Boolean, default=True, index=True)
    opened_at = Column(DateTime(timezone=True), server_default=func.now())
    closed_at = Column(DateTime(timezone=True), nullable=True)


class PnlRecord(Base):
    __tablename__ = "pnl_records"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime(timezone=True), nullable=False, index=True)
    portfolio_value = Column(Float, nullable=False)
    daily_pnl = Column(Float, default=0.0)
    cumulative_pnl = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class BotState(Base):
    __tablename__ = "bot_state"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String(20), default="stopped")  # running, paused, stopped
    mode = Column(String(10), default="paper")  # paper, live
    started_at = Column(DateTime(timezone=True), nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class ErrorLog(Base):
    __tablename__ = "error_logs"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(String(10), default="ERROR")
    message = Column(Text, nullable=False)
    traceback = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
