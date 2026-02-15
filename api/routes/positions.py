from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from api.database import get_db
from api.models import Position
from api.schemas import PositionOut

router = APIRouter(prefix="/positions", tags=["positions"])


@router.get("/", response_model=list[PositionOut])
async def get_positions(
    open_only: bool = Query(True),
    db: AsyncSession = Depends(get_db),
):
    query = select(Position).order_by(desc(Position.opened_at))
    if open_only:
        query = query.where(Position.is_open.is_(True))
    result = await db.execute(query)
    return result.scalars().all()
