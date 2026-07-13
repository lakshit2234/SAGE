"""Write generated doc artifacts to a branch and open a PR via PyGithub."""
from __future__ import annotations

import time
from pathlib import Path

from github import Auth, Github

from sage.core.logging import get_logger
from sage.db.models import DocArtifact
from sage.services.git_ops import clone_or_update_repo

log = get_logger(__name__)


def _write_artifacts_to_disk(local_path: Path, artifacts: list[DocArtifact]) -> list[str]:
    """Writes artifact content to their target file paths inside the local clone.
    Returns list of relative paths written."""
    written: list[str] = []
    for a in artifacts:
        target = local_path / a.file_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(a.content, encoding="utf-8")
        written.append(a.file_path)
    return written


def open_docs_pr(
    owner: str,
    name: str,
    access_token: str,
    base_branch: str,
    artifacts: list[DocArtifact],
    doc_run_id: str,
) -> dict:
    """Clones repo, checks out a new branch, writes artifacts, commits, pushes, opens PR.
    Runs git operations via GitPython (already used in git_ops) then uses PyGithub for the PR."""
    import git

    local_path = clone_or_update_repo(owner, name, access_token, branch=base_branch)
    repo = git.Repo(local_path)

    branch_name = f"sage/docs-update-{int(time.time())}"
    repo.git.checkout("-b", branch_name)

    written_paths = _write_artifacts_to_disk(local_path, artifacts)

    repo.git.add(all=True)
    if not repo.index.diff("HEAD"):
        log.info("pr_bot_no_changes", owner=owner, name=name)
        repo.git.checkout(base_branch)
        repo.git.branch("-D", branch_name)
        return {"status": "skipped", "reason": "no content changes vs existing files"}

    repo.index.commit(f"docs: SAGE auto-generated documentation update\n\ndoc_run_id={doc_run_id}")

    origin = repo.remotes.origin
    auth_url = f"https://x-access-token:{access_token}@github.com/{owner}/{name}.git"
    origin.set_url(auth_url)
    origin.push(refspec=f"{branch_name}:{branch_name}")

    auth = Auth.Token(access_token)
    gh = Github(auth=auth)
    gh_repo = gh.get_repo(f"{owner}/{name}")

    file_list = "\n".join(f"- `{p}`" for p in written_paths)
    pr_body = (
        f"## 🤖 SAGE Auto-Generated Documentation\n\n"
        f"This PR was opened automatically by **SAGE** after detecting new commits.\n\n"
        f"**Files updated:**\n{file_list}\n\n"
        f"_doc_run_id: `{doc_run_id}`_\n\n"
        f"Please review before merging — SAGE-generated content should be checked for accuracy."
    )

    pr = gh_repo.create_pull(
        title="docs: SAGE auto-generated documentation update",
        body=pr_body,
        head=branch_name,
        base=base_branch,
    )

    # reset local branch back to base for cleanliness
    repo.git.checkout(base_branch)

    log.info("pr_bot_opened", owner=owner, name=name, pr_number=pr.number, branch=branch_name)
    return {"status": "opened", "pr_number": pr.number, "pr_url": pr.html_url, "branch": branch_name}