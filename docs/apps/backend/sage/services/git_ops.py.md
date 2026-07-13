### Purpose Summary

The `git_ops.py` module provides functionality to clone and update GitHub repositories into a local workspace using an OAuth token. It includes methods for cloning new repositories, updating existing ones, retrieving the latest commit SHA, and listing source files within a repository.

### Key Functions/Classes

| Function/Class | Description |
|----------------|-------------|
| `_repo_dir(owner: str, name: str) -> Path` | Returns the local path where a repository should be stored based on its owner and name. |
| `clone_or_update_repo(owner: str, name: str, access_token: str, branch: str = "main") -> Path` | Clones a repository if it doesn't exist locally or updates it to the latest commit on the specified branch using the provided OAuth token. Returns the local path of the repository. |
| `get_head_commit_sha(local_path: Path) -> str` | Retrieves the SHA hash of the latest commit in the specified local repository. |
| `list_source_files(local_path: Path, extensions: set[str] | None = None) -> list[Path]` | Lists all trackable source files within a local repository, excluding common directories and file types like `.git`, `node_modules`, etc.

### Notable Dependencies and Side Effects

- **Dependencies**: This module relies on the `gitpython` library for interacting with Git repositories.
- **Side Effects**: The functions may modify the local filesystem by cloning or updating repositories. They also log information about repository operations using a logger configured in the `sage.core.logging` module.