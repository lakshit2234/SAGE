### Purpose Summary

The `vector_store.py` module provides a wrapper around ChromaDB to manage code-chunk embeddings for repositories. It allows embedding and querying code chunks based on semantic similarity.

### Key Functions/Classes

| Function/Class | Description |
|----------------|-------------|
| `get_chroma_client()` | Initializes and returns the ChromaDB client, ensuring it is created only once. |
| `_collection_name(owner: str, name: str) -> str` | Generates a safe collection name for a repository based on its owner and name. |
| `get_or_create_collection(owner: str, name: str)` | Retrieves an existing collection or creates a new one if it doesn't exist. |
| `upsert_chunks(owner: str, name: str, chunks: list[CodeChunk]) -> int` | Embeds and upserts code chunks into the specified repository's collection. Returns the count of successfully upserted chunks. |
| `query_similar(owner: str, name: str, query_text: str, n_results: int = 8) -> list[dict]` | Performs a semantic search over the code chunks in the specified repository and returns similar results. |

### Notable Dependencies

- **ChromaDB**: The primary database for storing and querying embeddings.
- **sage.core.config**: Used to retrieve configuration settings, specifically the path where ChromaDB should store its data.
- **sage.core.logging**: Provides logging functionality to log important events and warnings.
- **sage.services.chunker.CodeChunk**: Represents a code chunk with various attributes like file path, language, etc.
- **sage.services.embeddings.embed_batch** and **sage.services.embeddings.embed_text**: Functions for embedding text data into vector representations.

### Side Effects

- Creates directories if they do not exist (`settings.chroma_path`).
- Logs warnings when chunks are skipped due to embedding failures.
- Logs informational messages upon successful upserts and queries.