"""Current-user info and their GitHub repos."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request

from sage.services.github_auth import fetch_user_repos

router = APIRouter(tags=["users"])


def _require_token(request: Request) -> str:
    token = request.session.get("gh_access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated. Visit /auth/github/login")
    return token


@router.get("/auth/me")
async def me(request: Request) -> dict[str, str | None]:
    _require_token(request)
    return {
        "login": request.session.get("gh_login"),
        "avatar_url": request.session.get("gh_avatar_url"),
    }


@router.get("/repos/github")
async def list_github_repos(request: Request) -> list[dict]:
    token = _require_token(request)
    repos = await fetch_user_repos(token)
    return [
        {
            "id": r["id"],
            "full_name": r["full_name"],
            "owner": r["owner"]["login"],
            "name": r["name"],
            "private": r["private"],
            "default_branch": r.get("default_branch", "main"),
            "updated_at": r.get("updated_at"),
        }
        for r in repos
    ]