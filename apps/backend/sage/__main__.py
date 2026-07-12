"""Dev entrypoint: python -m sage"""
from __future__ import annotations

import uvicorn

from sage.core.config import get_settings


def main() -> None:
    settings = get_settings()
    uvicorn.run(
        "sage.app:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.app_env == "dev",
        log_level=settings.log_level.lower(),
    )


if __name__ == "__main__":
    main()