"""Celery application: background task queue backed by Redis (already running via docker compose)."""
from __future__ import annotations

from celery import Celery

from sage.core.config import get_settings

_settings = get_settings()

celery_app = Celery(
    "sage",
    broker=_settings.redis_url,
    backend=_settings.redis_url,
    include=["sage.workers.tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    worker_prefetch_multiplier=1,  # one task at a time: LLM/GPU work shouldn't be parallelized on 1 GPU
    task_acks_late=True,
)