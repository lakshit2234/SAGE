### Purpose Summary

The `api_extractor.py` module is designed to extract HTTP route definitions from Python (FastAPI/Flask) and JavaScript/TypeScript (Express) code using Tree-sitter. This ensures that routes are found deterministically rather than relying on LLM-guessed information, providing a reliable way to document and manage API endpoints.

### Key Functions/Classes

| Function/Class | Description |
|----------------|-------------|
| `ApiRoute` | A dataclass representing an HTTP route with details like method, path, file path, line number, handler name, and handler code. |
| `_extract_python_routes(file_path: Path, repo_root: Path) -> list[ApiRoute]` | Extracts HTTP routes from Python files using regular expressions. |
| `_extract_js_routes(file_path: Path, repo_root: Path) -> list[ApiRoute]` | Extracts HTTP routes from JavaScript/TypeScript files using regular expressions. |
| `extract_routes(repo_root: Path, files: list[Path]) -> list[ApiRoute]` | Scans all specified source files for HTTP route definitions and returns a list of `ApiRoute` objects. |
| `routes_to_markdown_table(routes: list[ApiRoute]) -> str` | Converts a list of `ApiRoute` objects into a Markdown table format, suitable for documentation or reporting. |

### Notable Dependencies and Side Effects

- **Dependencies**: The module uses the `re` module for regular expression matching to extract route information from source code.
- **Side Effects**: The module logs warnings if it fails to extract routes from certain files, but does not raise exceptions. It also logs an informational message when all routes have been extracted.

This module is integral to the larger system by providing a structured and deterministic way to document API endpoints across different programming languages and frameworks, facilitating easier maintenance and understanding of the application's API surface.