"""Health / readiness endpoints."""
from __future__ import annotations

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from sage.services.health import check_all

router = APIRouter(tags=["health"])


@router.get("/live")
async def liveness() -> dict[str, str]:
    """Cheap check: process is running."""
    return {"status": "alive"}


@router.get("/health")
async def health() -> JSONResponse:
    """Deep check: pings every dependency."""
    results = await check_all()
    payload = {
        "status": "ok" if all(r.ok for r in results) else "degraded",
        "components": [r.__dict__ for r in results],
    }
    code = status.HTTP_200_OK if payload["status"] == "ok" else status.HTTP_503_SERVICE_UNAVAILABLE
    return JSONResponse(content=payload, status_code=code)