"""Combine route extraction + LLM to produce an API reference doc."""
from __future__ import annotations

from pathlib import Path

from sage.core.logging import get_logger
from sage.services.api_extractor import ApiRoute, extract_routes, routes_to_markdown_table
from sage.services.git_ops import list_source_files
from sage.services.llm import generate
from sage.services.prompts import API_DOC_SYSTEM, api_doc_prompt

log = get_logger(__name__)

_MAX_HANDLER_SAMPLE_CHARS = 6000


def _sample_handler_code(routes: list[ApiRoute], repo_root: Path, limit: int = 15) -> str:
    """Pull the actual source lines around each route's handler for LLM context."""
    seen_files: dict[str, list[str]] = {}
    blocks: list[str] = []
    total = 0

    for r in routes[:limit]:
        if r.file_path not in seen_files:
            full_path = repo_root / r.file_path
            try:
                seen_files[r.file_path] = full_path.read_text(encoding="utf-8", errors="replace").splitlines()
            except Exception:  # noqa: BLE001
                continue
        file_lines = seen_files[r.file_path]
        start = max(0, r.line - 1)
        end = min(len(file_lines), start + 20)
        snippet = "\n".join(file_lines[start:end])
        block = f"# {r.file_path}:{r.line} -> {r.method} {r.path}\n{snippet}\n"
        if total + len(block) > _MAX_HANDLER_SAMPLE_CHARS:
            continue
        blocks.append(block)
        total += len(block)

    return "\n".join(blocks)


async def generate_api_docs(repo_name: str, local_path: Path) -> tuple[str, int]:
    """Returns (markdown_doc, route_count). If no routes found, returns a short notice."""
    files = list_source_files(local_path)
    routes = extract_routes(local_path, files)

    if not routes:
        return "_No HTTP API routes were detected in this repository._", 0

    table = routes_to_markdown_table(routes)
    handler_sample = _sample_handler_code(routes, local_path)

    prompt = api_doc_prompt(repo_name, table, handler_sample)
    text = await generate(prompt, system=API_DOC_SYSTEM, temperature=0.2, max_tokens=1800)

    full_doc = f"{text.strip()}\n\n## Route Reference\n\n{table}\n"
    return full_doc, len(routes)