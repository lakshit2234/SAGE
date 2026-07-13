# `apps/backend/sage/services/prompts.py`

This module contains various prompt templates for generating documentation from source code. These prompts are designed to be used by an AI language model (SAGE) to understand the context and content of a repository or specific file, and then generate appropriate documentation.

## Key Functions

### `readme_prompt(repo_name: str, file_summaries: list[str], sample_code: str) -> str`

- **Purpose**: Generates a professional README.md for a given repository.
- **Parameters**:
  - `repo_name`: The name of the repository.
  - `file_summaries`: A list of summaries of detected files in the repository.
  - `sample_code`: Representative code snippets from the repository.
- **Returns**: A Markdown formatted string representing the README.md.

### `module_doc_prompt(file_path: str, code: str) -> str`

- **Purpose**: Generates technical documentation for a specific source file.
- **Parameters**:
  - `file_path`: The path to the source file.
  - `code`: The content of the source file.
- **Returns**: A Markdown formatted string representing the documentation.

### `docstring_prompt(language: str, code: str) -> str`

- **Purpose**: Generates precise docstrings for undocumented code.
- **Parameters**:
  - `language`: The programming language of the code (e.g., Python).
  - `code`: The content of the function or class to document.
- **Returns**: A string containing the generated docstring.

### `api_doc_prompt(repo_name: str, routes_table: str, sample_handlers: str) -> str`

- **Purpose**: Generates API documentation for a repository based on detected routes and handler code.
- **Parameters**:
  - `repo_name`: The name of the repository.
  - `routes_table`: A table or list of detected routes.
  - `sample_handlers`: Sample implementations of route handlers.
- **Returns**: A Markdown formatted string representing the API documentation.

## How It Fits into the Larger System

This module is part of a larger system designed to automate the generation of technical documentation from source code. The prompts defined here serve as instructions for an AI language model (SAGE) on how to interpret and document different aspects of a software project, such as its README, individual modules, specific functions/classes, and REST APIs.

The generated documentation can then be used by developers to understand the structure, functionality, and usage of the codebase more effectively. This automation helps in reducing manual effort and ensures consistency across the documentation.