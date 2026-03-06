from typing import Any

from fastapi import APIRouter
from sqlalchemy import text

from app.db.session import SessionDependency

router = APIRouter(prefix="/health")


@router.get("/live")
async def liveness() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/ready")
async def readiness(session: SessionDependency) -> dict[str, Any]:
    try:
        await session.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception:
        db_status = "error"

    app_status = "ok" if db_status == "ok" else "degraded"
    return {"status": app_status, "checks": {"database": db_status}}
