## Purpose Summary

The `sage/services/chunker.py` module provides functionality for splitting source files into function/class-level chunks using the Tree-sitter parser. This is useful for analyzing code structure, generating documentation, or performing other operations at a higher level of abstraction than individual lines of code.

## Key Functions/Classes

| Function/Class | Description |
|----------------|-------------|
| `CodeChunk` | A dataclass representing a chunk of code, including its file path, language, node type, name, line numbers, and content. |
| `_extract_name(node, source)` | Extracts the name (if any) from a Tree-sitter node, typically used for function or class names. |
| `_walk(node, lang, source, file_rel, chunks)` | Recursively walks through a Tree-sitter parse tree to identify and extract code chunks based on specified node types. |
| `chunk_file(file_path: Path, repo_root: Path) -> list[CodeChunk]` | Parses a single file using Tree-sitter and extracts function/class-level chunks. |
| `chunk_repository(repo_root: Path, files: list[Path]) -> list[CodeChunk]` | Processes multiple files in a repository, extracting code chunks from each.

## Notable Dependencies and Side Effects

- **Dependencies**: This module relies on the `tree_sitter_language_pack` package for parsing source files with Tree-sitter. It also uses the `sage.core.logging` module for logging.
- **Side Effects**: The functions do not have significant side effects beyond reading file contents, parsing them, and creating data structures to store chunk information. They log warnings if parsing fails but otherwise operate in a read-only manner.