"""GitHub OAuth: authorize URL, token exchange, current-user fetch."""
from __future__ import annotations

import secrets
from typing import Any

import httpx

from sage.core.config import get_settings

GITHUB_AUTHORIZE_URL = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
GITHUB_API_BASE = "https://api.github.com"


def build_authorize_url(state: str | None = None) -> tuple[str, str]:
    settings = get_settings()
    state = state or secrets.token_urlsafe(24)
    params = {
        "client_id": settings.github_oauth_client_id,
        "redirect_uri": settings.github_oauth_callback_url,
        "scope": "repo read:user",
        "state": state,
    }
    query = "&".join(f"{k}={httpx.QueryParams({k: v})[k]}" for k, v in params.items())
    return f"{GITHUB_AUTHORIZE_URL}?{query}", state


async def exchange_code_for_token(code: str) -> str:
    settings = get_settings()
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.post(
            GITHUB_TOKEN_URL,
            headers={"Accept": "application/json"},
            data={
                "client_id": settings.github_oauth_client_id,
                "client_secret": settings.github_oauth_client_secret,
                "code": code,
                "redirect_uri": settings.github_oauth_callback_url,
            },
        )
        resp.raise_for_status()
        data = resp.json()
    if "error" in data:
        raise ValueError(f"GitHub OAuth error: {data.get('error_description', data['error'])}")
    return data["access_token"]


async def fetch_github_user(access_token: str) -> dict[str, Any]:
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(
            f"{GITHUB_API_BASE}/user",
            headers={"Authorization": f"Bearer {access_token}", "Accept": "application/vnd.github+json"},
        )
        resp.raise_for_status()
        return resp.json()


async def fetch_user_repos(access_token: str, per_page: int = 100) -> list[dict[str, Any]]:
    """Repos the authenticated user owns or collaborates on."""
    repos: list[dict[str, Any]] = []
    page = 1
    async with httpx.AsyncClient(timeout=10.0) as client:
        while True:
            resp = await client.get(
                f"{GITHUB_API_BASE}/user/repos",
                headers={"Authorization": f"Bearer {access_token}", "Accept": "application/vnd.github+json"},
                params={"per_page": per_page, "page": page, "sort": "updated"},
            )
            resp.raise_for_status()
            batch = resp.json()
            repos.extend(batch)
            if len(batch) < per_page:
                break
            page += 1
    return repos