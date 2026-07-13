"""Core ORM models: Repository, DocRun, DocArtifact, CommitEvent."""
from __future__ import annotations

import enum
import uuid

from sqlalchemy import Enum, ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sage.db.base import Base, TimestampMixin


class DocRunStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"


class ArtifactType(str, enum.Enum):
    README = "readme"
    MODULE_DOC = "module_doc"
    API_DOC = "api_doc"
    ARCHITECTURE_DIAGRAM = "architecture_diagram"
    DOCSTRING_PATCH = "docstring_patch"


class Repository(TimestampMixin, Base):
    __tablename__ = "repositories"
    __table_args__ = (UniqueConstraint("owner", "name", name="uq_repo_owner_name"),)

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    owner: Mapped[str] = mapped_column(String(255), index=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    default_branch: Mapped[str] = mapped_column(String(100), default="main")
    github_installation_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    github_access_token: Mapped[str | None] = mapped_column(String(255), nullable=True)  # dev-only; encrypt in prod
    is_active: Mapped[bool] = mapped_column(default=True)
    last_indexed_commit_sha: Mapped[str | None] = mapped_column(String(64), nullable=True)

    doc_runs: Mapped[list["DocRun"]] = relationship(
        back_populates="repository", cascade="all, delete-orphan"
    )

    @property
    def full_name(self) -> str:
        return f"{self.owner}/{self.name}"


class DocRun(TimestampMixin, Base):
    """One documentation-generation pass, triggered manually or by a commit."""
    __tablename__ = "doc_runs"
    __table_args__ = (Index("ix_doc_runs_repo_status", "repository_id", "status"),)

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    repository_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("repositories.id", ondelete="CASCADE")
    )
    triggered_by: Mapped[str] = mapped_column(String(50), default="manual")  # manual|webhook|schedule
    commit_sha: Mapped[str | None] = mapped_column(String(64), nullable=True)
    status: Mapped[DocRunStatus] = mapped_column(
        Enum(DocRunStatus, name="doc_run_status"), default=DocRunStatus.PENDING
    )
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    stats: Mapped[dict] = mapped_column(JSONB, default=dict)  # files scanned, tokens used, etc.

    repository: Mapped["Repository"] = relationship(back_populates="doc_runs")
    artifacts: Mapped[list["DocArtifact"]] = relationship(
        back_populates="doc_run", cascade="all, delete-orphan"
    )


class DocArtifact(TimestampMixin, Base):
    """A single generated output: a README, a diagram, an API doc page, etc."""
    __tablename__ = "doc_artifacts"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    doc_run_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("doc_runs.id", ondelete="CASCADE")
    )
    artifact_type: Mapped[ArtifactType] = mapped_column(Enum(ArtifactType, name="artifact_type"))
    file_path: Mapped[str] = mapped_column(String(1024))  # relative path in target repo
    content: Mapped[str] = mapped_column(Text)
    content_hash: Mapped[str] = mapped_column(String(64), index=True)

    doc_run: Mapped["DocRun"] = relationship(back_populates="artifacts")


class CommitEvent(TimestampMixin, Base):
    """Raw webhook event log, for audit + debugging incremental updates."""
    __tablename__ = "commit_events"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    repository_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("repositories.id", ondelete="CASCADE")
    )
    commit_sha: Mapped[str] = mapped_column(String(64))
    author: Mapped[str | None] = mapped_column(String(255), nullable=True)
    message: Mapped[str | None] = mapped_column(Text, nullable=True)
    payload: Mapped[dict] = mapped_column(JSONB, default=dict)