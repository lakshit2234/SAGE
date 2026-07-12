"""Tree-sitter based code chunker: splits source files into function/class-level chunks."""
from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path

from tree_sitter_language_pack import get_parser

from sage.core.logging import get_logger

log = get_logger(__name__)

_LANG_BY_EXT = {
    ".py": "python",
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "typescript",
    ".tsx": "tsx",
}

# node types considered "chunk-worthy" per language
_CHUNK_NODE_TYPES = {
    "python": {"function_definition", "class_definition", "decorated_definition"},
    "javascript": {
        "function_declaration",
        "class_declaration",
        "method_definition",
        "arrow_function",
        "lexical_declaration",  # covers `const foo = () => {}`
    },
    "typescript": {
        "function_declaration",
        "class_declaration",
        "method_definition",
        "arrow_function",
        "lexical_declaration",
        "interface_declaration",
        "type_alias_declaration",
    },
    "tsx": {
        "function_declaration",
        "class_declaration",
        "method_definition",
        "arrow_function",
        "lexical_declaration",
        "interface_declaration",
        "type_alias_declaration",
    },
}


@dataclass
class CodeChunk:
    file_path: str          # relative to repo root
    language: str
    node_type: str
    name: str | None        # function/class name if extractable
    start_line: int
    end_line: int
    code: str
    chunk_hash: str


def _extract_name(node, source: bytes) -> str | None:
    for child in node.children:
        if child.type in ("identifier", "property_identifier", "type_identifier"):
            return source[child.start_byte:child.end_byte].decode("utf-8", errors="replace")
    return None


def _walk(node, lang: str, source: bytes, file_rel: str, chunks: list[CodeChunk]) -> None:
    chunk_types = _CHUNK_NODE_TYPES.get(lang, set())
    if node.type in chunk_types:
        code = source[node.start_byte:node.end_byte].decode("utf-8", errors="replace")
        if len(code.strip()) > 10:  # skip trivial/empty matches
            chunk_hash = hashlib.sha256(code.encode("utf-8")).hexdigest()
            chunks.append(
                CodeChunk(
                    file_path=file_rel,
                    language=lang,
                    node_type=node.type,
                    name=_extract_name(node, source),
                    start_line=node.start_point[0] + 1,
                    end_line=node.end_point[0] + 1,
                    code=code,
                    chunk_hash=chunk_hash,
                )
            )
            return  # don't descend into an already-captured chunk (avoid nested dupes)
    for child in node.children:
        _walk(child, lang, source, file_rel, chunks)


def chunk_file(file_path: Path, repo_root: Path) -> list[CodeChunk]:
    lang = _LANG_BY_EXT.get(file_path.suffix)
    if lang is None:
        return []

    try:
        source = file_path.read_bytes()
        parser = get_parser(lang)
        tree = parser.parse(source)
    except Exception as exc:  # noqa: BLE001
        log.warning("chunk_parse_failed", file=str(file_path), error=str(exc))
        return []

    rel = str(file_path.relative_to(repo_root)).replace("\\", "/")
    chunks: list[CodeChunk] = []
    _walk(tree.root_node, lang, source, rel, chunks)
    return chunks


def chunk_repository(repo_root: Path, files: list[Path]) -> list[CodeChunk]:
    all_chunks: list[CodeChunk] = []
    for f in files:
        all_chunks.extend(chunk_file(f, repo_root))
    log.info("chunk_repository_done", files=len(files), chunks=len(all_chunks))
    return all_chunks