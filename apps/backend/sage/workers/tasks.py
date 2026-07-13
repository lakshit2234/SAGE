"""Celery tasks: async wrappers around the doc pipeline."""
from __future__ import annotations

import asyncio

from sage.core.logging import get_logger
from sage.workers.celery_app import celery_app

log = get_logger(__name__)


@celery_app.task(name="sage.run_doc_pipeline", bind=True, max_retries=2)
def run_doc_pipeline_task(self, owner: str, name: str, access_token: str) -> dict:
    """Sync entrypoint Celery calls; runs the async pipeline via asyncio.run."""
    from sage.services.pipeline import run_full_pipeline

    log.info("celery_task_start", owner=owner, name=name, task_id=self.request.id)
    try:
        result = asyncio.run(run_full_pipeline(owner, name, access_token, triggered_by="webhook"))
        log.info("celery_task_done", owner=owner, name=name, result=result)
        return result
    except Exception as exc:  # noqa: BLE001
        log.error("celery_task_failed", owner=owner, name=name, error=str(exc))
        raise self.retry(exc=exc, countdown=10) from exc