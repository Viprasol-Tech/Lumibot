"""FastAPI backend for the trading bot dashboard."""

import sys
from contextlib import asynccontextmanager
from pathlib import Path

# Ensure project root is on sys.path
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.database import init_db
from api.routes import trades, positions, dashboard, bot_control, settings
from bot.config import settings as app_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title="Trading Bot API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(trades.router, prefix="/api")
app.include_router(positions.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")
app.include_router(bot_control.router, prefix="/api")
app.include_router(settings.router, prefix="/api")


@app.get("/api/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "api.main:app",
        host=app_settings.API_HOST,
        port=app_settings.API_PORT,
        reload=True,
    )
