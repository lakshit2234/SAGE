"""Render a module dependency graph as a Mermaid flowchart, grouped by top-level folder
to stay readable (avoids a hairball of 70+ file-level nodes)."""
from __future__ import annotations

from collections import defaultdict

from sage.services.dependency_graph import ModuleNode


def _top_level_group(file_path: str) -> str:
    parts = file_path.split("/")
    if len(parts) <= 1:
        return "root"
    # group by parent directory (e.g. "apps/backend/sage/services/llm.py" -> "sage/services")
    return "/".join(parts[-3:-1]) if len(parts) >= 3 else "/".join(parts[:-1])


def _sanitize_id(name: str) -> str:
    return "".join(c if c.isalnum() else "_" for c in name)


def render_module_graph(nodes: list[ModuleNode], max_group_edges: int = 60) -> str:
    """Groups modules into folders, draws edges between groups. Returns Mermaid source."""
    if not nodes:
        return "flowchart TD\n    empty[\"No internal dependencies detected\"]"

    id_to_group: dict[str, str] = {}
    for n in nodes:
        id_to_group[n.id] = _top_level_group(n.file_path)

    group_edges: dict[tuple[str, str], int] = defaultdict(int)
    groups: set[str] = set()

    for n in nodes:
        src_group = id_to_group[n.id]
        groups.add(src_group)
        for imported_id in n.imports:
            dst_group = id_to_group.get(imported_id)
            if dst_group is None or dst_group == src_group:
                continue
            group_edges[(src_group, dst_group)] += 1

    lines = ["flowchart TD"]
    for g in sorted(groups):
        gid = _sanitize_id(g)
        lines.append(f'    {gid}["{g}"]')

    edges_sorted = sorted(group_edges.items(), key=lambda kv: -kv[1])[:max_group_edges]
    for (src, dst), weight in edges_sorted:
        src_id, dst_id = _sanitize_id(src), _sanitize_id(dst)
        label = f"|{weight}|" if weight > 1 else ""
        lines.append(f"    {src_id} -->{label} {dst_id}")

    return "\n".join(lines)