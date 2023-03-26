import uvicorn

from guarantor.settings import settings
from guarantor.web.application import app


def main() -> None:
    """Entrypoint of the application."""
    uvicorn.run(
        "guarantor.web.application:get_app_for_uvicorn",
        workers=settings.workers_count,
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level.value.lower(),
        factory=True,
    )


if __name__ == "__main__":
    main()
