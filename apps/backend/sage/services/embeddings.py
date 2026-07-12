"""Embed text via Ollama (nomic-embed-text), running locally on GPU."""
from __future__ import annotations

import asyncio

import httpx

from sage.core.config import get_settings
from sage.core.logging import get_logger

log = get_logger(__name__)

_MAX_RETRIES = 3
_MAX_CHARS = 6000  # ~ safe char budget to avoid overloading nomic-embed-text context


async def embed_text(text: str) -> list[float] | None:
    """Returns None if embedding permanently fails (caller should skip that chunk)."""
    settings = get_settings()
    text = text[:_MAX_CHARS]
    last_exc: Exception | None = None
    async with httpx.AsyncClient(timeout=60.0) as client:
        for attempt in range(1, _MAX_RETRIES + 1):
            try:
                resp = await client.post(
                    f"{settings.ollama_base_url}/api/embeddings",
                    json={"model": settings.ollama_embed_model, "prompt": text},
                )
                resp.raise_for_status()
                return resp.json()["embedding"]
            except (httpx.HTTPStatusError, httpx.TransportError) as exc:
                last_exc = exc
                log.warning("embed_retry", attempt=attempt, error=str(exc), text_len=len(text))
                await asyncio.sleep(0.5 * attempt)
    log.error("embed_permanently_failed", error=str(last_exc), text_len=len(text))
    return None


async def embed_batch(texts: list[str], concurrency: int = 1) -> list[list[float] | None]:
    """Embed many texts sequentially (concurrency=1 default). Failed items come back as None."""
    sem = asyncio.Semaphore(concurrency)

    async def _one(t: str) -> list[float] | None:
        async with sem:
            return await embed_text(t)

    return await asyncio.gather(*[_one(t) for t in texts])