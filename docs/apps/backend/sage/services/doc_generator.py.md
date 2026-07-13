# `doc_generator.py`

## Purpose

The `doc_generator.py` module is responsible for generating documentation artifacts by combining retrieved code chunks with the output of a Large Language Model (LLM). It selects representative code snippets from the chunks, constructs prompts based on these snippets, and then uses the LLM to generate either READMEs or module-level documentation.

## Key Functions/Classes

| Function/Class | Description |
|----------------|-------------|
| `_select_representative_chunks(chunks: list[CodeChunk], limit_chars: int = _MAX_SAMPLE_CHARS) -> str` | Greedily packs the largest/most central code chunks into a budget, prioritizing named classes/functions and longer snippets. |
| `generate_readme(repo_name: str, local_path: Path, chunks: list[CodeChunk]) -> str` | Asynchronously generates a README for a repository by selecting representative code snippets and using an LLM prompt. |
| `generate_module_doc(file_path: str, code: str) -> str` | Asynchronously generates documentation for a single module by using an LLM prompt with the provided file path and code snippet. |
| `content_hash(text: str) -> str` | Generates a SHA-256 hash of the given text to ensure content integrity or caching purposes. |

## Dependencies

- **sage.core.logging**: For logging purposes.
- **sage.services.chunker.CodeChunk**: Represents individual code chunks retrieved from source files.
- **sage.services.git_ops.list_source_files(local_path: Path) -> list[Path]**: Lists source files in a given local path.
- **sage.services.llm.generate(prompt, system=README_SYSTEM/MODULE_DOC_SYSTEM, temperature=0.2, max_tokens=1800/900)**: Asynchronously generates text using an LLM based on the provided prompt and parameters.
- **sage.services.prompts**: Contains prompts for README and module documentation generation.

## Side Effects

- The module performs asynchronous operations that may involve I/O and network calls to generate documentation.
- It logs information using the `get_logger` function from `sage.core.logging`.