"""ChromaDB wrapper: one collection per repository, storing code-chunk embeddings."""
from __future__ import annotations

from pathlib import Path

import chromadb
from chromadb.config import Settings as ChromaSettings

from sage.core.config import get_settings
from sage.core.logging import get_logger
from sage.services.chunker import CodeChunk
from sage.services.embeddings import embed_batch

log = get_logger(__name__)

_client: chromadb.ClientAPI | None = None


def get_chroma_client() -> chromadb.ClientAPI:
    global _client
    if _client is None:
        settings = get_settings()
        Path(settings.chroma_path).mkdir(parents=True, exist_ok=True)
        _client = chromadb.PersistentClient(
            path=settings.chroma_path,
            settings=ChromaSettings(anonymized_telemetry=False),
        )
    return _client


def _collection_name(owner: str, name: str) -> str:
    # Chroma collection names: 3-63 chars, alnum/underscore/hyphen only
    safe = f"{owner}_{name}".lower().replace("/", "_")
    return "".join(c if c.isalnum() or c in "_-" else "_" for c in safe)[:63]


def get_or_create_collection(owner: str, name: str):
    client = get_chroma_client()
    return client.get_or_create_collection(
        name=_collection_name(owner, name),
        metadata={"owner": owner, "repo": name},
    )


async def upsert_chunks(owner: str, name: str, chunks: list[CodeChunk]) -> int:
    """Embed and upsert all chunks for a repo. Returns count upserted."""
    if not chunks:
        return 0

    collection = get_or_create_collection(owner, name)

    texts = [f"# {c.file_path}\n{c.code}" for c in chunks]
    embeddings = await embed_batch(texts)

    # drop chunks whose embedding permanently failed
    kept = [(c, e) for c, e in zip(chunks, embeddings) if e is not None]
    skipped = len(chunks) - len(kept)
    if skipped:
        log.warning("vector_upsert_skipped_chunks", owner=owner, name=name, skipped=skipped)

    if not kept:
        return 0

    ids = [f"{c.file_path}::{c.start_line}-{c.end_line}::{c.chunk_hash[:12]}" for c, _ in kept]
    metadatas = [
        {
            "file_path": c.file_path,
            "language": c.language,
            "node_type": c.node_type,
            "name": c.name or "",
            "start_line": c.start_line,
            "end_line": c.end_line,
            "chunk_hash": c.chunk_hash,
        }
        for c, _ in kept
    ]
    docs = [c.code for c, _ in kept]
    embeds = [e for _, e in kept]

    collection.upsert(ids=ids, embeddings=embeds, documents=docs, metadatas=metadatas)
    log.info("vector_upsert_done", owner=owner, name=name, count=len(kept))
    return len(kept)


async def query_similar(owner: str, name: str, query_text: str, n_results: int = 8) -> list[dict]:
    """Semantic search over a repo's chunks."""
    from sage.services.embeddings import embed_text

    collection = get_or_create_collection(owner, name)
    query_embedding = await embed_text(query_text)

    results = collection.query(query_embeddings=[query_embedding], n_results=n_results)

    out: list[dict] = []
    docs = results.get("documents") or [[]]
    metas = results.get("metadatas") or [[]]
    dists = results.get("distances") or [[]]
    for doc, meta, dist in zip(docs[0], metas[0], dists[0]):
        out.append({"code": doc, "metadata": meta, "distance": dist})
    return out