from fastapi import APIRouter

from api.schemas import StrategySettings

router = APIRouter(prefix="/settings", tags=["settings"])

# In-memory settings store (persists for the lifetime of the API process).
_current_settings = StrategySettings()


@router.get("/", response_model=StrategySettings)
async def get_settings():
    return _current_settings


@router.put("/", response_model=StrategySettings)
async def update_settings(new_settings: StrategySettings):
    global _current_settings
    _current_settings = new_settings
    return _current_settings
