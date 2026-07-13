"""Prompt templates for doc generation."""
from __future__ import annotations

README_SYSTEM = """You are SAGE, an expert technical writer and software architect.
You generate clear, accurate, professional documentation directly from source code.
Never invent functionality that isn't in the code. Use Markdown. Be concise but complete."""


def readme_prompt(repo_name: str, file_summaries: list[str], sample_code: str) -> str:
    joined = "\n".join(f"- {s}" for s in file_summaries)
    return f"""Generate a professional README.md for the repository "{repo_name}".

Files detected:
{joined}

Representative code (most relevant chunks):
{sample_code}
Write a README with these sections: Title, Description, Features, Installation, Usage, Project Structure.
Base every claim strictly on the code shown. If installation steps aren't inferable, write a reasonable
generic instruction (e.g. "pip install -r requirements.txt") rather than guessing specifics."""


MODULE_DOC_SYSTEM = """You are SAGE, generating per-module technical documentation from source code.
Explain purpose, key functions/classes, and how the module fits into the larger system. Use Markdown."""


def module_doc_prompt(file_path: str, code: str) -> str:
    return f"""Document this source file: `{file_path}`

{code}

Produce Markdown with: a one-paragraph purpose summary, a table of key functions/classes with
one-line descriptions, and any notable dependencies or side effects."""


DOCSTRING_SYSTEM = """You are SAGE, generating precise docstrings for undocumented code.
Return ONLY the docstring content (no code, no markdown fences), following the language's convention
(Google-style for Python, JSDoc for JS/TS)."""


def docstring_prompt(language: str, code: str) -> str:
    return f"""Language: {language}

Function/class:

{code}

Write only the docstring for this, describing purpose, parameters, and return value."""

API_DOC_SYSTEM = """You are SAGE, documenting a REST API from its detected routes and handler code.
Write clear, accurate endpoint descriptions. Never invent parameters or behavior not shown in the code."""


def api_doc_prompt(repo_name: str, routes_table: str, sample_handlers: str) -> str:
    return f"""Generate API documentation for "{repo_name}".

Detected routes:
{routes_table}

Sample handler implementations:
{sample_handlers}

Write a Markdown API reference: a brief intro paragraph, then for each meaningfully distinct
endpoint, a short description of what it does based on the handler code. Group by resource/path prefix
if there's a clear pattern. Do not invent request/response schemas that aren't visible in the code."""