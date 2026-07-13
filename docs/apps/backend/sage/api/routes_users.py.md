# `apps/backend/sage/api/routes_users.py`

## Purpose

This module defines FastAPI routes related to user information and their GitHub repositories. It provides endpoints for retrieving the current authenticated user's details and listing their GitHub repositories.

## Key Functions/Classes

| Function/Class | Description |
|----------------|-------------|
| `_require_token(request: Request) -> str` | Retrieves the GitHub access token from the session, raising an HTTP 401 error if not authenticated. |
| `me(request: Request) -> dict[str, str | None]` | Returns the current authenticated user's login and avatar URL. |
| `list_github_repos(request: Request) -> list[dict]` | Lists the GitHub repositories associated with the current authenticated user, including details such as repository ID, full name, owner, name, privacy status, default branch, and last update time. |

## Dependencies

- **FastAPI**: The module uses FastAPI for defining and handling HTTP routes.
- **sage.services.github_auth.fetch_user_repos(token: str) -> list[dict]**: This function is called to fetch the user's GitHub repositories using the provided access token.

## Side Effects

- Raises an `HTTPException` with a status code of 401 if the user is not authenticated.
- Retrieves and uses data from the session to authenticate requests.