# LLM Generation Service (llm.py)

The `llm.py` module provides services for generating language model responses using the Ollama Qwen2.5-Coder model via local GPU inference. It includes both single-shot and streaming generation capabilities.

## Key Functions/Classes

| Function/Class | Description |
|----------------|-------------|
| `generate(prompt: str, system: str | None = None, temperature: float = 0.2, max_tokens: int = 2048) -> str` | Asynchronously generates a single-shot response to the given prompt using the specified parameters. |
| `generate_stream(prompt: str, system: str | None = None, temperature: float = 0.2, max_tokens: int = 2048) -> AsyncIterator[str]` | Asynchronously streams text chunks as they are generated for the given prompt. |

## Notable Dependencies and Side Effects

- **Dependencies**: The module depends on `httpx` for making HTTP requests to the Ollama API.
- **Side Effects**: The module logs warnings if retries occur during generation, which can be configured via the application settings.

This module is integral to the backend services that require language model responses, providing both synchronous and asynchronous options for generating text based on user input.