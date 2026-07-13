### Purpose Summary

The `routes_repos.py` module in the SAGE backend provides API endpoints for managing GitHub repositories. It allows users to connect a repository, clone it locally, run a chunker on its source files, and store the chunks in a vector database. The module also includes functionality to list connected repositories and search for similar code chunks within them.

### Key Functions/Classes

| Function/Class | Description |
|----------------|-------------|
| `_require_token(request: Request) -> str` | Retrieves the GitHub access token from the request session, raising an HTTPException if not authenticated. |
| `connect_repo(request: Request, body: ConnectRepoRequest, session: AsyncSession = Depends(get_session)) -> Repository` | Handles the POST request to connect a repository by cloning it, running the chunker, and storing the chunks in the vector database. |
| `list_connected_repos(session: AsyncSession = Depends(get_session)) -> list[Repository]` | Retrieves a list of all connected repositories that are currently active. |
| `search_repo_chunks(owner: str, name: str, q: str, k: int = 8) -> list[dict]` | Searches for similar code chunks within a specified repository using the provided query string and returns up to `k` results. |

### Notable Dependencies and Side Effects

- **Dependencies**: The module depends on several services such as `chunk_repository`, `clone_or_update_repo`, `get_head_commit_sha`, `list_source_files`, `query_similar`, and `upsert_chunks`. It also uses a database session (`AsyncSession`) to interact with the repository data.
- **Side Effects**: When connecting a repository, the module clones it locally, runs a chunker on its source files, and stores the chunks in a vector database. This can result in disk space usage and potential network activity depending on the size of the repository and the number of files involved.