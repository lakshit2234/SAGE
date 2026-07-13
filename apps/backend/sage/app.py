"""FastAPI application factory."""
from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from sage.api.routes_auth import router as auth_router
from sage.api.routes_health import router as health_router
from sage.api.routes_repos import router as repos_router
from sage.api.routes_docs import router as docs_router
from sage.api.routes_webhooks import router as webhooks_router
from sage.api.routes_users import router as users_router
from sage.core.config import get_settings
from sage.core.logging import configure_logging, get_logger


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ARG001
    configure_logging()
    log = get_logger("sage.app")
    settings = get_settings()
    log.info("sage_startup", env=settings.app_env, port=settings.app_port)
    yield
    log.info("sage_shutdown")


def create_app() -> FastAPI:
    app = FastAPI(
        title="SAGE",
        description="Self-updating Autonomous Generator for Engineering-docs",
        version="0.1.0",
        lifespan=lifespan,
    )

    app.add_middleware(SessionMiddleware, secret_key=get_settings().session_secret)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health_router)
    app.include_router(auth_router)
    app.include_router(users_router)
    app.include_router(repos_router)
    app.include_router(docs_router)
    app.include_router(webhooks_router)

    @app.get("/", tags=["root"])
    async def root() -> dict[str, str]:
        return {"name": "SAGE", "version": "0.1.0", "docs": "/docs"}

    return app


app = create_app()