# GitHub OAuth Service

The `github_auth.py` module provides functionality for handling GitHub OAuth authentication, including generating an authorization URL, exchanging an authorization code for an access token, fetching the current user's information, and retrieving a list of repositories owned by or collaborated on by the authenticated user.

## Key Functions/Classes

| Function/Class | Description |
|----------------|-------------|
| `build_authorize_url(state: str | None = None) -> tuple[str, str]` | Generates an authorization URL for GitHub OAuth. |
| `exchange_code_for_token(code: str) -> str` | Exchanges a GitHub authorization code for an access token. |
| `fetch_github_user(access_token: str) -> dict[str, Any]` | Fetches the current user's information from GitHub using their access token. |
| `fetch_user_repos(access_token: str, per_page: int = 100) -> list[dict[str, Any]]` | Retrieves a list of repositories owned by or collaborated on by the authenticated user. |

## Dependencies and Side Effects

- **Dependencies**: This module depends on the `httpx` library for making HTTP requests to GitHub's API.
- **Side Effects**: The functions in this module do not have significant side effects beyond making network requests and handling responses.

This module is integral to integrating GitHub authentication into the larger system, allowing users to authenticate using their GitHub accounts and access their repositories.