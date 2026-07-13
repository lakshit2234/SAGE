### Purpose Summary

The `dependency_graph.py` module is responsible for building a module dependency graph from import statements in Python and JavaScript/TypeScript files within a repository. It uses regular expressions to extract import statements and resolves them to internal modules, ensuring that only imports within the same repository are considered. The resulting graph can be used for various purposes such as visualizing dependencies, analyzing code structure, or optimizing build processes.

### Key Functions/Classes

| Function/Class | Description |
| --- | --- |
| `ModuleNode` | A data class representing a module in the dependency graph, containing its ID, file path, and set of imported modules. |
| `_normalize_py_module(local_path: Path, repo_root: Path) -> str` | Normalizes a Python module path to be used as a node ID in the graph. |
| `_resolve_py_import(module: str, all_py_modules: set[str]) -> str | None` | Resolves a Python import statement to an internal module within the repository. |
| `_resolve_js_import(from_file: Path, rel_import: str, repo_root: Path) -> str | None` | Resolves a JavaScript/TypeScript import statement to an internal module within the repository. |
| `build_dependency_graph(repo_root: Path, files: list[Path]) -> list[ModuleNode]` | Builds and returns a list of `ModuleNode` objects representing the dependency graph for the given files in the repository. |

### Notable Dependencies or Side Effects

- **Dependencies**: The module relies on Python's built-in `re` (regular expression) module, `dataclasses`, `pathlib`, and `sage.core.logging`. It also uses the `get_logger` function from the `sage.core.logging` module to log information about the graph building process.
- **Side Effects**: The `_normalize_py_module` function modifies the file path by replacing backslashes with forward slashes and converting it to a dotted format. The `_resolve_js_import` function attempts to resolve relative paths by appending various suffixes (e.g., `.js`, `.ts`) and checking if the resulting file exists. If an error occurs while reading a file, the module logs an error message but continues processing other files.