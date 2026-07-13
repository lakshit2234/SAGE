"""Connect a GitHub repo, clone it, and run the chunker."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from sage.db.base import get_session
from sage.db.models import Repository
from sage.schemas.repository import ConnectRepoRequest, RepositoryOut
from sage.services.chunker import chunk_repository
from sage.services.git_ops import clone_or_update_repo, get_head_commit_sha, list_source_files
from sage.services.vector_store import query_similar, upsert_chunks
from sage.core.logging import get_logger

log = get_logger(__name__)
router = APIRouter(prefix="/repos", tags=["repos"])


def _require_token(request: Request) -> str:
    token = request.session.get("gh_access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated. Visit /auth/github/login")
    return token


@router.post("/connect", response_model=RepositoryOut)
async def connect_repo(
    request: Request,
    body: ConnectRepoRequest,
    session: AsyncSession = Depends(get_session),
) -> Repository:
    token = _require_token(request)

    existing = await session.scalar(
        select(Repository).where(Repository.owner == body.owner, Repository.name == body.name)
    )
    if existing:
        repo_row = existing
    else:
        repo_row = Repository(owner=body.owner, name=body.name, default_branch=body.default_branch)
        session.add(repo_row)
        await session.flush()

    local_path = clone_or_update_repo(body.owner, body.name, token, branch=body.default_branch)
    sha = get_head_commit_sha(local_path)

    files = list_source_files(local_path)
    chunks = chunk_repository(local_path, files)
    embedded_count = await upsert_chunks(body.owner, body.name, chunks)

    repo_row.last_indexed_commit_sha = sha
    repo_row.is_active = True
    repo_row.github_access_token = token
    await session.commit()
    await session.refresh(repo_row)

    log.info(
        "repo_connected",
        owner=body.owner,
        name=body.name,
        files=len(files),
        chunks=len(chunks),
        embedded=embedded_count,
        sha=sha,
    )
    return repo_row


@router.get("", response_model=list[RepositoryOut])
async def list_connected_repos(session: AsyncSession = Depends(get_session)) -> list[Repository]:
    result = await session.scalars(select(Repository).where(Repository.is_active.is_(True)))
    return list(result.all())

@router.get("/{owner}/{name}/search")
async def search_repo_chunks(owner: str, name: str, q: str, k: int = 8) -> list[dict]:
    return await query_similar(owner, name, q, n_results=k)