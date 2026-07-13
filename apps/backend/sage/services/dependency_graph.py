"""Build a module dependency graph from import statements (Python + JS/TS),
using regex extraction — deterministic, no LLM guessing involved."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from sage.core.logging import get_logger

log = get_logger(__name__)

_PY_IMPORT_RE = re.compile(r"^\s*(?:from\s+([\w.]+)\s+import|import\s+([\w.]+))", re.MULTILINE)
_JS_IMPORT_RE = re.compile(r"""(?:import\s+.*?from\s+|require\s*\(\s*)['"](\.[^'"]+)['"]""")


@dataclass
class ModuleNode:
    id: str            # normalized module path, used as diagram node id
    file_path: str      # relative file path
    imports: set[str] = field(default_factory=set)  # ids of modules it imports (internal only)


def _normalize_py_module(local_path: Path, repo_root: Path) -> str:
    rel = local_path.relative_to(repo_root).with_suffix("")
    return str(rel).replace("\\", "/").replace("/", ".")


def _resolve_py_import(module: str, all_py_modules: set[str]) -> str | None:
    """Only keep imports that resolve to a module inside this repo."""
    candidates = [module, module.split(".")[0]]
    for c in candidates:
        if c in all_py_modules:
            return c
        # try matching by suffix (e.g. `sage.services.llm` resolves partial paths)
        matches = [m for m in all_py_modules if m == c or m.endswith("." + c)]
        if matches:
            return matches[0]
    return None


def _resolve_js_import(from_file: Path, rel_import: str, repo_root: Path) -> str | None:
    target = (from_file.parent / rel_import).resolve()
    for suffix in ("", ".js", ".ts", ".jsx", ".tsx", "/index.js", "/index.ts"):
        candidate = Path(str(target) + suffix)
        if candidate.exists():
            try:
                rel = candidate.relative_to(repo_root).with_suffix("")
                return str(rel).replace("\\", "/")
            except ValueError:
                return None
    return None


def build_dependency_graph(repo_root: Path, files: list[Path]) -> list[ModuleNode]:
    py_files = [f for f in files if f.suffix == ".py"]
    js_files = [f for f in files if f.suffix in (".js", ".ts", ".jsx", ".tsx")]

    py_module_ids = {_normalize_py_module(f, repo_root) for f in py_files}
    nodes: dict[str, ModuleNode] = {}

    for f in py_files:
        mod_id = _normalize_py_module(f, repo_root)
        node = ModuleNode(id=mod_id, file_path=str(f.relative_to(repo_root)).replace("\\", "/"))
        try:
            source = f.read_text(encoding="utf-8", errors="replace")
        except Exception:  # noqa: BLE001
            nodes[mod_id] = node
            continue
        for m in _PY_IMPORT_RE.finditer(source):
            raw = m.group(1) or m.group(2)
            if not raw:
                continue
            resolved = _resolve_py_import(raw, py_module_ids)
            if resolved and resolved != mod_id:
                node.imports.add(resolved)
        nodes[mod_id] = node

    for f in js_files:
        mod_id = str(f.relative_to(repo_root).with_suffix("")).replace("\\", "/")
        node = ModuleNode(id=mod_id, file_path=str(f.relative_to(repo_root)).replace("\\", "/"))
        try:
            source = f.read_text(encoding="utf-8", errors="replace")
        except Exception:  # noqa: BLE001
            nodes[mod_id] = node
            continue
        for m in _JS_IMPORT_RE.finditer(source):
            resolved = _resolve_js_import(f, m.group(1), repo_root)
            if resolved and resolved != mod_id:
                node.imports.add(resolved)
        nodes[mod_id] = node

    log.info("dependency_graph_built", nodes=len(nodes))
    return list(nodes.values())