import logging
from importlib import metadata

from fastapi import FastAPI
from fastapi.responses import UJSONResponse
from tortoise.contrib.fastapi import register_tortoise

from guarantor.common.socketio import asgi_app, sio
from guarantor.db.config import TORTOISE_CONFIG
from guarantor.logging import configure_logging
from guarantor.socketio.chat.handlers import sio_connect_handler, sio_message_handler
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

    # Socket IO handlers
    sio.on("connect", handler=sio_connect_handler)
    sio.on("message", handler=sio_message_handler)

    app.mount("/", asgi_app)

    return app
