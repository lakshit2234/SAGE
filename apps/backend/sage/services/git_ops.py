"""Clone / pull GitHub repos to local workspace, using the OAuth token."""
from __future__ import annotations

from pathlib import Path

import git

from sage.core.config import get_settings
from sage.core.logging import get_logger

log = get_logger(__name__)


def _repo_dir(owner: str, name: str) -> Path:
    settings = get_settings()
    return Path(settings.repos_dir) / owner / name


def clone_or_update_repo(owner: str, name: str, access_token: str, branch: str = "main") -> Path:
    """Clone the repo if absent, else fetch + reset to latest on `branch`. Returns local path."""
    dest = _repo_dir(owner, name)
    dest.parent.mkdir(parents=True, exist_ok=True)

    auth_url = f"https://x-access-token:{access_token}@github.com/{owner}/{name}.git"

    if dest.exists() and (dest / ".git").exists():
        log.info("repo_update", owner=owner, name=name)
        repo = git.Repo(dest)
        origin = repo.remotes.origin
        origin.set_url(auth_url)
        origin.fetch()
        repo.git.checkout(branch)
        repo.git.reset("--hard", f"origin/{branch}")
    else:
        log.info("repo_clone", owner=owner, name=name)
        repo = git.Repo.clone_from(auth_url, dest, branch=branch)

    return dest


def get_head_commit_sha(local_path: Path) -> str:
    repo = git.Repo(local_path)
    return repo.head.commit.hexsha


def list_source_files(local_path: Path, extensions: set[str] | None = None) -> list[Path]:
    """List trackable source files, skipping .git, node_modules, venv, etc."""
    extensions = extensions or {".py", ".js", ".jsx", ".ts", ".tsx"}
    skip_dirs = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build", ".next"}

    files: list[Path] = []
    for path in local_path.rglob("*"):
        if not path.is_file():
            continue
        if any(part in skip_dirs for part in path.parts):
            continue
        if path.suffix in extensions:
            files.append(path)
    return files