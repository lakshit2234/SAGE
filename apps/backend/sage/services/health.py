"""Health probes for Postgres, Redis, Ollama."""
from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Any

import asyncpg
import httpx
import redis.asyncio as aioredis

from sage.core.config import get_settings
from sage.core.logging import get_logger

log = get_logger(__name__)


@dataclass
class ComponentStatus:
    name: str
    ok: bool
    detail: str = ""


async def check_postgres() -> ComponentStatus:
    settings = get_settings()
    try:
        conn = await asyncio.wait_for(
            asyncpg.connect(settings.postgres_dsn), timeout=3.0
        )
        try:
            version = await conn.fetchval("SELECT version();")
        finally:
            await conn.close()
        return ComponentStatus("postgres", True, str(version).split(",")[0])
    except Exception as exc:  # noqa: BLE001
        log.warning("postgres_health_failed", error=str(exc))
        return ComponentStatus("postgres", False, str(exc))


async def check_redis() -> ComponentStatus:
    settings = get_settings()
    try:
        client = aioredis.from_url(settings.redis_url, socket_timeout=3, protocol=2)
        pong = await client.ping()
        await client.aclose()
        return ComponentStatus("redis", bool(pong), "PONG" if pong else "no reply")
    except Exception as exc:  # noqa: BLE001
        log.warning("redis_health_failed", error=str(exc))
        return ComponentStatus("redis", False, str(exc))


async def check_ollama() -> ComponentStatus:
    settings = get_settings()
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            r = await client.get(f"{settings.ollama_base_url}/api/tags")
            r.raise_for_status()
            data: dict[str, Any] = r.json()
            models = [m["name"] for m in data.get("models", [])]
        want = {settings.ollama_llm_model, settings.ollama_embed_model}
        missing = [m for m in want if not any(m in name for name in models)]
        ok = not missing
        detail = "models present" if ok else f"missing: {missing}"
        return ComponentStatus("ollama", ok, detail)
    except Exception as exc:  # noqa: BLE001
        log.warning("ollama_health_failed", error=str(exc))
        return ComponentStatus("ollama", False, str(exc))


async def check_all() -> list[ComponentStatus]:
    return list(
        await asyncio.gather(
            check_postgres(),
            check_redis(),
            check_ollama(),
        )
    )