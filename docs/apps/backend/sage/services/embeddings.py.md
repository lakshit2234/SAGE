### Purpose Summary

The `embeddings.py` module provides services for embedding text using the Ollama (nomic-embed-text) model running locally on a GPU. It includes asynchronous functions to embed individual texts and batches of texts with optional concurrency.

### Key Functions/Classes

| Function/Class | Description |
|----------------|-------------|
| `embed_text(text: str) -> list[float] | None` | Asynchronously embeds a single text string using Ollama's API. Returns the embedding as a list of floats or `None` if the embedding permanently fails. |
| `embed_batch(texts: list[str], concurrency: int = 1) -> list[list[float] | None]` | Asynchronously embeds multiple text strings in batches with optional concurrency. Failed items are returned as `None`. |

### Notable Dependencies and Side Effects

- **Dependencies**: The module depends on the `httpx` library for making HTTP requests to Ollama's API, and it uses settings from `sage.core.config.get_settings()` to determine the base URL and embedding model.
- **Side Effects**: Logging is performed using `sage.core.logging.get_logger(__name__)`, which logs warnings when retries fail and errors when permanent failures occur. The module also handles rate limiting by sleeping for an increasing duration between retries.