import json
import logging
from importlib import metadata
from typing import Any

from fastapi import FastAPI, Depends, Request
from fastapi.responses import UJSONResponse
from loguru import logger
from tortoise.contrib.fastapi import register_tortoise

from guarantor.common.socketio import SocketIO
from guarantor.db.config import TORTOISE_CONFIG
from guarantor.logging import configure_logging
from guarantor.web.api.router import api_router
from guarantor.web.lifetime import register_shutdown_event, register_startup_event


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    configure_logging()
    app = FastAPI(
        title="guarantor",
        version=metadata.version("guarantor"),
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
    )

    # Adds startup and shutdown events.
    register_startup_event(app)
    register_shutdown_event(app)

    # Main router for the API.
    app.include_router(router=api_router, prefix="/api")
    # Configures tortoise orm.
    register_tortoise(
        app,
        config=TORTOISE_CONFIG,
        add_exception_handlers=True,
    )
    logging.getLogger("socketio").setLevel(logging.DEBUG)
    logging.getLogger("engineio").setLevel(logging.DEBUG)

    return app


app = get_app()
s = SocketIO()


@s.sio.event
async def connect(sid, environ, auth) -> None:
    s.sio
    await s.sio.emit('a', {'hello': auth})
    #logger.info(args)
    #logger.info(kwargs)

app.mount("/", s.asgi_app)


def get_app_for_uvicorn():
    return app
