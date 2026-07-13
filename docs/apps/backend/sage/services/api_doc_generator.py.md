### Purpose Summary

The `api_doc_generator.py` module is responsible for generating API reference documentation by combining route extraction from source code with the use of a Large Language Model (LLM). It identifies HTTP routes in a repository, extracts relevant handler code snippets, and uses these to generate comprehensive API documentation in Markdown format.

### Key Functions/Classes

| Function/Class | Description |
|----------------|-------------|
| `_sample_handler_code(routes: list[ApiRoute], repo_root: Path, limit: int = 15) -> str` | Samples up to `limit` handler code snippets from the source files of detected routes for context in the LLM. |
| `generate_api_docs(repo_name: str, local_path: Path) -> tuple[str, int]` | Extracts API routes from a repository, generates an API reference document using an LLM, and returns the Markdown document along with the count of routes found. |

### Notable Dependencies or Side Effects

- **Dependencies**: This module relies on several other services such as `ApiRoute`, `extract_routes`, `routes_to_markdown_table`, `list_source_files`, `generate`, and `api_doc_prompt`. It also uses a logger for logging purposes.
  
- **Side Effects**: The `_sample_handler_code` function reads the content of source files, which can have side effects if file access fails or is restricted. The `generate_api_docs` function may generate large strings containing API documentation, which could impact memory usage.

This module plays a crucial role in automating the generation of API reference documents, making it easier for developers to understand and use APIs within their projects.