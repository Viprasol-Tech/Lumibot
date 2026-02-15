from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from api.database import get_db
from api.models import Trade
from api.schemas import TradeOut

router = APIRouter(prefix="/trades", tags=["trades"])


@router.get("/", response_model=list[TradeOut])
async def get_trades(
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    symbol: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    query = select(Trade).order_by(desc(Trade.created_at)).offset(offset).limit(limit)
    if symbol:
        query = query.where(Trade.symbol == symbol.upper())
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{trade_id}", response_model=TradeOut)
async def get_trade(trade_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Trade).where(Trade.id == trade_id))
    trade = result.scalar_one_or_none()
    if not trade:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Trade not found")
    return trade
