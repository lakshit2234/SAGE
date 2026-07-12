"""Ties together retrieved chunks + LLM to produce documentation artifacts."""
from __future__ import annotations

import hashlib
from pathlib import Path

from sage.core.logging import get_logger
from sage.services.chunker import CodeChunk
from sage.services.git_ops import list_source_files
from sage.services.llm import generate
from sage.services.prompts import (
    MODULE_DOC_SYSTEM,
    README_SYSTEM,
    module_doc_prompt,
    readme_prompt,
)

log = get_logger(__name__)

_MAX_SAMPLE_CHARS = 8000  # keep prompt within qwen2.5-coder's comfortable context on 7.8GB VRAM


def _select_representative_chunks(chunks: list[CodeChunk], limit_chars: int = _MAX_SAMPLE_CHARS) -> str:
    """Greedily pack the largest/most central chunks (by simple heuristic) into a budget."""
    # heuristic: prefer named classes/functions, then longest snippets first
    ranked = sorted(
        chunks,
        key=lambda c: (c.node_type in ("class_definition", "class_declaration"), len(c.code)),
        reverse=True,
    )
    out: list[str] = []
    total = 0
    for c in ranked:
        block = f"# {c.file_path} ({c.name or c.node_type})\n{c.code}\n"
        if total + len(block) > limit_chars:
            continue
        out.append(block)
        total += len(block)
        if total >= limit_chars:
            break
    return "\n".join(out)


async def generate_readme(repo_name: str, local_path: Path, chunks: list[CodeChunk]) -> str:
    files = list_source_files(local_path)
    file_summaries = [str(f.relative_to(local_path)).replace("\\", "/") for f in files[:40]]
    sample_code = _select_representative_chunks(chunks)

    prompt = readme_prompt(repo_name, file_summaries, sample_code)
    text = await generate(prompt, system=README_SYSTEM, temperature=0.2, max_tokens=1800)
    return text.strip()


async def generate_module_doc(file_path: str, code: str) -> str:
    prompt = module_doc_prompt(file_path, code[:_MAX_SAMPLE_CHARS])
    text = await generate(prompt, system=MODULE_DOC_SYSTEM, temperature=0.2, max_tokens=900)
    return text.strip()


def content_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()