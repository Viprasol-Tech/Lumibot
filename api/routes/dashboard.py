from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, desc, func
from sqlalchemy.ext.asyncio import AsyncSession

from api.database import get_db
from api.models import PnlRecord, Position, BotState
from api.schemas import DashboardOverview, PnlRecordOut

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/overview", response_model=DashboardOverview)
async def get_overview(db: AsyncSession = Depends(get_db)):
    # Latest P&L record
    pnl_result = await db.execute(
        select(PnlRecord).order_by(desc(PnlRecord.date)).limit(1)
    )
    latest_pnl = pnl_result.scalar_one_or_none()

    # Open positions count
    pos_result = await db.execute(
        select(func.count()).select_from(Position).where(Position.is_open.is_(True))
    )
    open_count = pos_result.scalar() or 0

    # Bot state
    state_result = await db.execute(select(BotState).order_by(desc(BotState.id)).limit(1))
    bot_state = state_result.scalar_one_or_none()

    return DashboardOverview(
        account_value=latest_pnl.portfolio_value if latest_pnl else 0.0,
        daily_pnl=latest_pnl.daily_pnl if latest_pnl else 0.0,
        open_positions=open_count,
        bot_status=bot_state.status if bot_state else "stopped",
        bot_mode=bot_state.mode if bot_state else "paper",
    )


@router.get("/pnl", response_model=list[PnlRecordOut])
async def get_pnl_history(
    limit: int = Query(90, ge=1, le=365),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(PnlRecord).order_by(desc(PnlRecord.date)).limit(limit)
    )
    records = result.scalars().all()
    return list(reversed(records))  # oldest first for charting
