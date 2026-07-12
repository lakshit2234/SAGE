"""Pydantic schemas for repository connect/read."""
from __future__ import annotations

import uuid

from pydantic import BaseModel


class ConnectRepoRequest(BaseModel):
    owner: str
    name: str
    default_branch: str = "main"


class RepositoryOut(BaseModel):
    id: uuid.UUID
    owner: str
    name: str
    default_branch: str
    is_active: bool
    last_indexed_commit_sha: str | None

    model_config = {"from_attributes": True}