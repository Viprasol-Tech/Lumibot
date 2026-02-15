import os

# Override DATABASE_URL before importing the app
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///./test.db"

import pytest
from httpx import AsyncClient, ASGITransport

from api.main import app
from api.database import engine, Base


@pytest.fixture(autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.anyio
async def test_health(client):
    resp = await client.get("/api/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


@pytest.mark.anyio
async def test_get_trades_empty(client):
    resp = await client.get("/api/trades/")
    assert resp.status_code == 200
    assert resp.json() == []


@pytest.mark.anyio
async def test_get_positions_empty(client):
    resp = await client.get("/api/positions/")
    assert resp.status_code == 200
    assert resp.json() == []


@pytest.mark.anyio
async def test_dashboard_overview(client):
    resp = await client.get("/api/dashboard/overview")
    assert resp.status_code == 200
    data = resp.json()
    assert "account_value" in data
    assert "bot_status" in data


@pytest.mark.anyio
async def test_bot_control_flow(client):
    resp = await client.post("/api/bot/control", json={"action": "start"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "running"

    resp = await client.post("/api/bot/control", json={"action": "pause"})
    assert resp.json()["status"] == "paused"

    resp = await client.post("/api/bot/control", json={"action": "stop"})
    assert resp.json()["status"] == "stopped"


@pytest.mark.anyio
async def test_settings_round_trip(client):
    new = {
        "symbol": "AAPL",
        "risk_per_trade": 0.03,
        "max_positions": 10,
        "stop_loss_pct": 0.03,
        "take_profit_pct": 0.06,
        "use_trailing_stop": True,
        "trailing_stop_pct": 0.02,
    }
    resp = await client.put("/api/settings/", json=new)
    assert resp.status_code == 200
    assert resp.json()["symbol"] == "AAPL"

    resp = await client.get("/api/settings/")
    assert resp.json()["risk_per_trade"] == 0.03
