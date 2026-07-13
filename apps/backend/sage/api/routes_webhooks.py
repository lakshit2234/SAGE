"""GitHub webhook receiver: verifies signature, enqueues a Celery doc-pipeline job."""
from __future__ import annotations

import hashlib
import hmac

from fastapi import APIRouter, Header, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from sage.core.config import get_settings
from sage.core.logging import get_logger
from sage.db.base import get_session
from sage.db.models import Repository

log = get_logger(__name__)
router = APIRouter(prefix="/webhooks", tags=["webhooks"])


def _verify_signature(payload_body: bytes, signature_header: str | None, secret: str) -> bool:
    if not signature_header or not secret:
        return False
    expected = "sha256=" + hmac.new(secret.encode(), payload_body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature_header)


@router.post("/github")
async def github_webhook(
    request: Request,
    session: AsyncSession = Depends(get_session),
    x_hub_signature_256: str | None = Header(default=None),
    x_github_event: str | None = Header(default=None),
) -> dict:
    body = await request.body()
    settings = get_settings()

    if not _verify_signature(body, x_hub_signature_256, settings.github_webhook_secret):
        raise HTTPException(status_code=401, detail="Invalid webhook signature")

    if x_github_event != "push":
        return {"status": "ignored", "reason": f"event type {x_github_event} not handled"}

    payload = await request.json()
    repo_info = payload.get("repository", {})
    owner = repo_info.get("owner", {}).get("login")
    name = repo_info.get("name")

    if not owner or not name:
        raise HTTPException(status_code=400, detail="Malformed payload: missing repository info")

    repo_row = await session.scalar(
        select(Repository).where(Repository.owner == owner, Repository.name == name)
    )
    if repo_row is None or not repo_row.github_access_token:
        log.warning("webhook_unknown_repo", owner=owner, name=name)
        return {"status": "ignored", "reason": "repo not connected to SAGE"}

    from sage.workers.tasks import run_doc_pipeline_task

    task = run_doc_pipeline_task.delay(owner, name, repo_row.github_access_token)
    log.info("webhook_enqueued", owner=owner, name=name, task_id=task.id)
    return {"status": "enqueued", "task_id": task.id}