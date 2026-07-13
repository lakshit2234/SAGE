"""Batch per-file documentation generation."""
from __future__ import annotations

import asyncio
from pathlib import Path

from sage.core.logging import get_logger
from sage.services.doc_generator import generate_module_doc
from sage.services.git_ops import list_source_files

log = get_logger(__name__)

_MIN_FILE_CHARS = 80          # skip near-empty files (e.g. bare __init__.py)
_MAX_FILE_CHARS = 12000       # skip huge files (would blow context budget)
_CONCURRENCY = 1              # sequential: local Ollama handles one generation well at a time


async def generate_module_docs(local_path: Path) -> list[dict]:
    """Returns list of {file_path, content} for every documentable file."""
    files = list_source_files(local_path)
    sem = asyncio.Semaphore(_CONCURRENCY)
    results: list[dict] = []

    async def _doc_one(f: Path) -> dict | None:
        text = f.read_text(encoding="utf-8", errors="replace")
        if len(text.strip()) < _MIN_FILE_CHARS:
            return None
        rel = str(f.relative_to(local_path)).replace("\\", "/")
        async with sem:
            try:
                doc = await generate_module_doc(rel, text[:_MAX_FILE_CHARS])
            except Exception as exc:  # noqa: BLE001
                log.warning("module_doc_failed", file=rel, error=str(exc))
                return None
        log.info("module_doc_generated", file=rel, chars=len(doc))
        return {"file_path": rel, "content": doc}

    for f in files:
        r = await _doc_one(f)
        if r:
            results.append(r)

    log.info("module_docs_batch_done", total_files=len(files), documented=len(results))
    return results