"""Trigger doc generation for a connected repo, persist results."""
from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from sage.core.config import get_settings
from sage.core.logging import get_logger
from sage.db.base import get_session
from sage.db.models import ArtifactType, DocArtifact, DocRun, DocRunStatus, Repository
from sage.services.chunker import chunk_repository
from sage.services.doc_generator import content_hash, generate_readme
from sage.services.git_ops import get_head_commit_sha, list_source_files
from sage.services.api_doc_generator import generate_api_docs
from sage.services.module_docs import generate_module_docs

log = get_logger(__name__)
router = APIRouter(prefix="/docs", tags=["docs"])


@router.post("/{owner}/{name}/generate/readme")
async def generate_readme_for_repo(
    owner: str, name: str, session: AsyncSession = Depends(get_session)
) -> dict:
    repo_row = await session.scalar(
        select(Repository).where(Repository.owner == owner, Repository.name == name)
    )
    if repo_row is None:
        raise HTTPException(status_code=404, detail="Repository not connected. POST /repos/connect first.")

    settings = get_settings()
    local_path = Path(settings.repos_dir) / owner / name
    if not local_path.exists():
        raise HTTPException(status_code=409, detail="Local clone missing. Reconnect the repo.")

    sha = get_head_commit_sha(local_path)
    files = list_source_files(local_path)
    chunks = chunk_repository(local_path, files)

    doc_run = DocRun(
        repository_id=repo_row.id,
        triggered_by="manual",
        commit_sha=sha,
        status=DocRunStatus.RUNNING,
        stats={"files": len(files), "chunks": len(chunks)},
    )
    session.add(doc_run)
    await session.flush()

    try:
        readme_text = await generate_readme(f"{owner}/{name}", local_path, chunks)
    except Exception as exc:  # noqa: BLE001
        doc_run.status = DocRunStatus.FAILED
        doc_run.error_message = str(exc)
        await session.commit()
        log.error("readme_generation_failed", owner=owner, name=name, error=str(exc))
        raise HTTPException(status_code=502, detail=f"LLM generation failed: {exc}") from exc

    artifact = DocArtifact(
        doc_run_id=doc_run.id,
        artifact_type=ArtifactType.README,
        file_path="README.generated.md",
        content=readme_text,
        content_hash=content_hash(readme_text),
    )
    session.add(artifact)

    doc_run.status = DocRunStatus.SUCCESS
    await session.commit()
    await session.refresh(artifact)

    log.info("readme_generated", owner=owner, name=name, doc_run_id=str(doc_run.id), chars=len(readme_text))
    return {
        "doc_run_id": str(doc_run.id),
        "artifact_id": str(artifact.id),
        "content": readme_text,
    }

@router.post("/{owner}/{name}/generate/modules")
async def generate_module_docs_for_repo(
    owner: str, name: str, session: AsyncSession = Depends(get_session)
) -> dict:
    repo_row = await session.scalar(
        select(Repository).where(Repository.owner == owner, Repository.name == name)
    )
    if repo_row is None:
        raise HTTPException(status_code=404, detail="Repository not connected. POST /repos/connect first.")

    settings = get_settings()
    local_path = Path(settings.repos_dir) / owner / name
    if not local_path.exists():
        raise HTTPException(status_code=409, detail="Local clone missing. Reconnect the repo.")

    sha = get_head_commit_sha(local_path)

    doc_run = DocRun(
        repository_id=repo_row.id,
        triggered_by="manual",
        commit_sha=sha,
        status=DocRunStatus.RUNNING,
        stats={},
    )
    session.add(doc_run)
    await session.flush()

    try:
        module_docs = await generate_module_docs(local_path)
    except Exception as exc:  # noqa: BLE001
        doc_run.status = DocRunStatus.FAILED
        doc_run.error_message = str(exc)
        await session.commit()
        log.error("module_docs_generation_failed", owner=owner, name=name, error=str(exc))
        raise HTTPException(status_code=502, detail=f"LLM generation failed: {exc}") from exc

    artifact_ids: list[str] = []
    for doc in module_docs:
        artifact = DocArtifact(
            doc_run_id=doc_run.id,
            artifact_type=ArtifactType.MODULE_DOC,
            file_path=f"docs/{doc['file_path']}.md",
            content=doc["content"],
            content_hash=content_hash(doc["content"]),
        )
        session.add(artifact)
        await session.flush()
        artifact_ids.append(str(artifact.id))

    doc_run.status = DocRunStatus.SUCCESS
    doc_run.stats = {"documented_files": len(module_docs)}
    await session.commit()

    log.info(
        "module_docs_generated_batch",
        owner=owner,
        name=name,
        doc_run_id=str(doc_run.id),
        count=len(module_docs),
    )
    return {
        "doc_run_id": str(doc_run.id),
        "artifact_count": len(artifact_ids),
        "artifact_ids": artifact_ids,
    }

@router.post("/{owner}/{name}/generate/api-docs")
async def generate_api_docs_for_repo(
    owner: str, name: str, session: AsyncSession = Depends(get_session)
) -> dict:
    repo_row = await session.scalar(
        select(Repository).where(Repository.owner == owner, Repository.name == name)
    )
    if repo_row is None:
        raise HTTPException(status_code=404, detail="Repository not connected. POST /repos/connect first.")

    settings = get_settings()
    local_path = Path(settings.repos_dir) / owner / name
    if not local_path.exists():
        raise HTTPException(status_code=409, detail="Local clone missing. Reconnect the repo.")

    sha = get_head_commit_sha(local_path)

    doc_run = DocRun(
        repository_id=repo_row.id,
        triggered_by="manual",
        commit_sha=sha,
        status=DocRunStatus.RUNNING,
        stats={},
    )
    session.add(doc_run)
    await session.flush()

    try:
        doc_text, route_count = await generate_api_docs(f"{owner}/{name}", local_path)
    except Exception as exc:  # noqa: BLE001
        doc_run.status = DocRunStatus.FAILED
        doc_run.error_message = str(exc)
        await session.commit()
        log.error("api_doc_generation_failed", owner=owner, name=name, error=str(exc))
        raise HTTPException(status_code=502, detail=f"LLM generation failed: {exc}") from exc

    artifact = DocArtifact(
        doc_run_id=doc_run.id,
        artifact_type=ArtifactType.API_DOC,
        file_path="docs/API.generated.md",
        content=doc_text,
        content_hash=content_hash(doc_text),
    )
    session.add(artifact)

    doc_run.status = DocRunStatus.SUCCESS
    doc_run.stats = {"routes_found": route_count}
    await session.commit()
    await session.refresh(artifact)

    log.info("api_docs_generated", owner=owner, name=name, doc_run_id=str(doc_run.id), routes=route_count)
    return {
        "doc_run_id": str(doc_run.id),
        "artifact_id": str(artifact.id),
        "routes_found": route_count,
        "content": doc_text,
    }

@router.get("/{owner}/{name}/runs")
async def list_doc_runs(owner: str, name: str, session: AsyncSession = Depends(get_session)) -> list[dict]:
    repo_row = await session.scalar(
        select(Repository).where(Repository.owner == owner, Repository.name == name)
    )
    if repo_row is None:
        raise HTTPException(status_code=404, detail="Repository not connected.")

    result = await session.scalars(
        select(DocRun).where(DocRun.repository_id == repo_row.id).order_by(DocRun.created_at.desc())
    )
    runs = result.all()
    return [
        {
            "id": str(r.id),
            "status": r.status.value,
            "commit_sha": r.commit_sha,
            "stats": r.stats,
            "created_at": r.created_at.isoformat(),
        }
        for r in runs
    ]