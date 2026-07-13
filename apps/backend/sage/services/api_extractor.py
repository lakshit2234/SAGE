"""Extract HTTP route definitions from Python (FastAPI/Flask) and JS/TS (Express) code
using Tree-sitter, so routes are found deterministically rather than LLM-guessed."""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from sage.core.logging import get_logger

log = get_logger(__name__)

_PY_DECORATOR_RE = re.compile(
    r"@(?:\w+\.)?(get|post|put|delete|patch|options|head|route)\s*\(\s*[\"']([^\"']+)[\"']"
)
_JS_ROUTE_RE = re.compile(
    r"\b(?:app|router)\.(get|post|put|delete|patch|options|head)\s*\(\s*[\"'`]([^\"'`]+)[\"'`]"
)


@dataclass
class ApiRoute:
    method: str
    path: str
    file_path: str
    line: int
    handler_name: str | None
    handler_code: str | None


def _extract_python_routes(file_path: Path, repo_root: Path) -> list[ApiRoute]:
    source = file_path.read_text(encoding="utf-8", errors="replace")
    rel = str(file_path.relative_to(repo_root)).replace("\\", "/")
    routes: list[ApiRoute] = []

    lines = source.splitlines()
    for i, line in enumerate(lines):
        m = _PY_DECORATOR_RE.search(line)
        if not m:
            continue
        method = m.group(1).upper()
        if method == "ROUTE":
            method = "GET"  # Flask's generic @app.route defaults to GET unless methods= specified
        path = m.group(2)

        # find the function name on the next non-blank line
        handler_name = None
        for j in range(i + 1, min(i + 4, len(lines))):
            fm = re.search(r"def\s+(\w+)\s*\(", lines[j])
            if fm:
                handler_name = fm.group(1)
                break

        routes.append(
            ApiRoute(
                method=method,
                path=path,
                file_path=rel,
                line=i + 1,
                handler_name=handler_name,
                handler_code=None,
            )
        )
    return routes


def _extract_js_routes(file_path: Path, repo_root: Path) -> list[ApiRoute]:
    source = file_path.read_text(encoding="utf-8", errors="replace")
    rel = str(file_path.relative_to(repo_root)).replace("\\", "/")
    routes: list[ApiRoute] = []

    for i, line in enumerate(source.splitlines()):
        m = _JS_ROUTE_RE.search(line)
        if not m:
            continue
        routes.append(
            ApiRoute(
                method=m.group(1).upper(),
                path=m.group(2),
                file_path=rel,
                line=i + 1,
                handler_name=None,
                handler_code=None,
            )
        )
    return routes


def extract_routes(repo_root: Path, files: list[Path]) -> list[ApiRoute]:
    """Scan all source files for HTTP route definitions."""
    all_routes: list[ApiRoute] = []
    for f in files:
        try:
            if f.suffix == ".py":
                all_routes.extend(_extract_python_routes(f, repo_root))
            elif f.suffix in (".js", ".ts", ".jsx", ".tsx"):
                all_routes.extend(_extract_js_routes(f, repo_root))
        except Exception as exc:  # noqa: BLE001
            log.warning("route_extract_failed", file=str(f), error=str(exc))
    log.info("routes_extracted", count=len(all_routes))
    return all_routes


def routes_to_markdown_table(routes: list[ApiRoute]) -> str:
    if not routes:
        return "_No HTTP routes detected._"
    lines = ["| Method | Path | Handler | Location |", "|---|---|---|---|"]
    for r in sorted(routes, key=lambda x: (x.path, x.method)):
        handler = r.handler_name or "-"
        loc = f"`{r.file_path}:{r.line}`"
        lines.append(f"| `{r.method}` | `{r.path}` | {handler} | {loc} |")
    return "\n".join(lines)