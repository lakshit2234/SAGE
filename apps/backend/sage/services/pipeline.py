"""Full documentation pipeline: clone -> chunk -> embed -> generate everything.
Shared by the manual connect endpoint and the Celery webhook task."""
from __future__ import annotations

from pathlib import Path

from sage.core.config import get_settings
from sage.core.logging import get_logger
from sage.db.base import async_session_factory
from sage.db.models import ArtifactType, DocArtifact, DocRun, DocRunStatus, Repository
from sage.services.api_doc_generator import generate_api_docs
from sage.services.chunker import chunk_repository
from sage.services.dependency_graph import build_dependency_graph
from sage.services.doc_generator import content_hash, generate_readme
from sage.services.git_ops import clone_or_update_repo, get_head_commit_sha, list_source_files
from sage.services.mermaid_renderer import render_module_graph
from sage.services.module_docs import generate_module_docs
from sage.services.vector_store import upsert_chunks
from sqlalchemy import select

log = get_logger(__name__)


async def run_full_pipeline(owner: str, name: str, access_token: str, triggered_by: str = "webhook") -> dict:
    """Clone/update, chunk, embed, and generate README + module docs + API docs + architecture.
    Returns a summary dict. Safe to call repeatedly (idempotent upserts)."""
    settings = get_settings()

    async with async_session_factory() as session:
        repo_row = await session.scalar(
            select(Repository).where(Repository.owner == owner, Repository.name == name)
        )
        if repo_row is None:
            repo_row = Repository(owner=owner, name=name)
            session.add(repo_row)
            await session.flush()

        local_path = clone_or_update_repo(owner, name, access_token, branch=repo_row.default_branch)
        sha = get_head_commit_sha(local_path)

        if repo_row.last_indexed_commit_sha == sha:
            log.info("pipeline_skip_no_changes", owner=owner, name=name, sha=sha)
            return {"status": "skipped", "reason": "no new commits", "sha": sha}

        files = list_source_files(local_path)
        chunks = chunk_repository(local_path, files)
        embedded = await upsert_chunks(owner, name, chunks)

        doc_run = DocRun(
            repository_id=repo_row.id,
            triggered_by=triggered_by,
            commit_sha=sha,
            status=DocRunStatus.RUNNING,
            stats={"files": len(files), "chunks": len(chunks), "embedded": embedded},
        )
        session.add(doc_run)
        await session.flush()

        artifacts_created = 0
        try:
            readme_text = await generate_readme(f"{owner}/{name}", local_path, chunks)
            session.add(DocArtifact(
                doc_run_id=doc_run.id, artifact_type=ArtifactType.README,
                file_path="README.generated.md", content=readme_text,
                content_hash=content_hash(readme_text),
            ))
            artifacts_created += 1

            module_docs = await generate_module_docs(local_path)
            for doc in module_docs:
                session.add(DocArtifact(
                    doc_run_id=doc_run.id, artifact_type=ArtifactType.MODULE_DOC,
                    file_path=f"docs/{doc['file_path']}.md", content=doc["content"],
                    content_hash=content_hash(doc["content"]),
                ))
            artifacts_created += len(module_docs)

            api_text, route_count = await generate_api_docs(f"{owner}/{name}", local_path)
            session.add(DocArtifact(
                doc_run_id=doc_run.id, artifact_type=ArtifactType.API_DOC,
                file_path="docs/API.generated.md", content=api_text,
                content_hash=content_hash(api_text),
            ))
            artifacts_created += 1

            nodes = build_dependency_graph(local_path, files)
            mermaid_src = render_module_graph(nodes)
            arch_content = f"# Architecture Diagram\n\n```mermaid\n{mermaid_src}\n```\n"
            session.add(DocArtifact(
                doc_run_id=doc_run.id, artifact_type=ArtifactType.ARCHITECTURE_DIAGRAM,
                file_path="docs/ARCHITECTURE.generated.md", content=arch_content,
                content_hash=content_hash(arch_content),
            ))
            artifacts_created += 1

        except Exception as exc:  # noqa: BLE001
            doc_run.status = DocRunStatus.FAILED
            doc_run.error_message = str(exc)
            await session.commit()
            log.error("pipeline_failed", owner=owner, name=name, error=str(exc))
            raise

        doc_run.status = DocRunStatus.SUCCESS
        doc_run.stats = {**doc_run.stats, "artifacts_created": artifacts_created, "routes_found": route_count}
        repo_row.last_indexed_commit_sha = sha
        repo_row.is_active = True
        await session.commit()

        log.info(
            "pipeline_complete", owner=owner, name=name, sha=sha,
            artifacts=artifacts_created, doc_run_id=str(doc_run.id),
        )
        return {
            "status": "success",
            "doc_run_id": str(doc_run.id),
            "sha": sha,
            "artifacts_created": artifacts_created,
        }