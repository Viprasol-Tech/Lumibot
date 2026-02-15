import logging
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from api.database import get_db
from api.models import BotState
from api.schemas import BotStatus, BotCommand

logger = logging.getLogger("trading_bot.api")

router = APIRouter(prefix="/bot", tags=["bot_control"])

# In-process reference to the running bot (set by the app on startup).
_bot_handle = None


def set_bot_handle(handle) -> None:
    global _bot_handle
    _bot_handle = handle


@router.get("/status", response_model=BotStatus)
async def get_bot_status(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(BotState).order_by(desc(BotState.id)).limit(1))
    state = result.scalar_one_or_none()
    if not state:
        return BotStatus(status="stopped", mode="paper")
    return BotStatus(status=state.status, mode=state.mode, started_at=state.started_at)


@router.post("/control", response_model=BotStatus)
async def control_bot(cmd: BotCommand, db: AsyncSession = Depends(get_db)):
    action = cmd.action.lower()
    if action not in ("start", "pause", "stop"):
        raise HTTPException(status_code=400, detail="Invalid action. Use start, pause, or stop.")

    result = await db.execute(select(BotState).order_by(desc(BotState.id)).limit(1))
    state = result.scalar_one_or_none()

    if not state:
        state = BotState(status="stopped", mode="paper")
        db.add(state)

    if action == "start":
        state.status = "running"
        state.started_at = datetime.now(timezone.utc)
        logger.info("Bot started via API")
    elif action == "pause":
        state.status = "paused"
        logger.info("Bot paused via API")
    elif action == "stop":
        state.status = "stopped"
        logger.info("Bot stopped via API")

    await db.commit()
    await db.refresh(state)
    return BotStatus(status=state.status, mode=state.mode, started_at=state.started_at)
