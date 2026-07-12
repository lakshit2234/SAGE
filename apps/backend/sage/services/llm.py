"""LLM generation via Ollama (qwen2.5-coder), local GPU inference."""
from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator

import httpx

from sage.core.config import get_settings
from sage.core.logging import get_logger

log = get_logger(__name__)

_MAX_RETRIES = 3
_DEFAULT_TIMEOUT = 180.0  # 7B model on 7.8GB VRAM: allow generous time for long generations


async def generate(
    prompt: str,
    system: str | None = None,
    temperature: float = 0.2,
    max_tokens: int = 2048,
) -> str:
    """Single-shot (non-streaming) generation. Returns full text."""
    settings = get_settings()
    payload = {
        "model": settings.ollama_llm_model,
        "prompt": prompt,
        "system": system or "",
        "stream": False,
        "options": {
            "temperature": temperature,
            "num_predict": max_tokens,
        },
    }

    last_exc: Exception | None = None
    async with httpx.AsyncClient(timeout=_DEFAULT_TIMEOUT) as client:
        for attempt in range(1, _MAX_RETRIES + 1):
            try:
                resp = await client.post(f"{settings.ollama_base_url}/api/generate", json=payload)
                resp.raise_for_status()
                return resp.json()["response"]
            except (httpx.HTTPStatusError, httpx.TransportError) as exc:
                last_exc = exc
                log.warning("llm_generate_retry", attempt=attempt, error=str(exc))
                await asyncio.sleep(1.0 * attempt)
    raise last_exc  # noqa: RSE102


async def generate_stream(
    prompt: str,
    system: str | None = None,
    temperature: float = 0.2,
    max_tokens: int = 2048,
) -> AsyncIterator[str]:
    """Streaming generation: yields text chunks as they're produced."""
    settings = get_settings()
    payload = {
        "model": settings.ollama_llm_model,
        "prompt": prompt,
        "system": system or "",
        "stream": True,
        "options": {
            "temperature": temperature,
            "num_predict": max_tokens,
        },
    }

    import json

    async with httpx.AsyncClient(timeout=_DEFAULT_TIMEOUT) as client:
        async with client.stream("POST", f"{settings.ollama_base_url}/api/generate", json=payload) as resp:
            resp.raise_for_status()
            async for line in resp.aiter_lines():
                if not line:
                    continue
                chunk = json.loads(line)
                if chunk.get("response"):
                    yield chunk["response"]
                if chunk.get("done"):
                    break