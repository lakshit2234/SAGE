"""GitHub OAuth login flow."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse

from sage.core.logging import get_logger
from sage.services.github_auth import (
    build_authorize_url,
    exchange_code_for_token,
    fetch_github_user,
)

log = get_logger(__name__)
router = APIRouter(prefix="/auth/github", tags=["auth"])


@router.get("/login")
async def login(request: Request) -> RedirectResponse:
    url, state = build_authorize_url()
    request.session["oauth_state"] = state
    return RedirectResponse(url)


@router.get("/callback")
async def callback(request: Request, code: str, state: str) -> RedirectResponse:
    expected_state = request.session.get("oauth_state")
    if not expected_state or expected_state != state:
        raise HTTPException(status_code=400, detail="Invalid OAuth state")

    try:
        token = await exchange_code_for_token(code)
        user = await fetch_github_user(token)
    except Exception as exc:  # noqa: BLE001
        log.warning("github_oauth_failed", error=str(exc))
        raise HTTPException(status_code=502, detail="GitHub OAuth exchange failed") from exc

    request.session["gh_access_token"] = token
    request.session["gh_login"] = user.get("login")
    request.session["gh_avatar_url"] = user.get("avatar_url")
    request.session.pop("oauth_state", None)

    log.info("github_login_success", login=user.get("login"))
    return RedirectResponse("/auth/me")


@router.get("/logout")
async def logout(request: Request) -> dict[str, str]:
    request.session.clear()
    return {"status": "logged_out"}