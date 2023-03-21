import logging
from importlib import metadata

import socketio
from fastapi import FastAPI
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
    logging.getLogger('socketio').setLevel(logging.DEBUG)
    logging.getLogger('engineio').setLevel(logging.DEBUG)

    #sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins=["*"])
    #asgi_app = socketio.ASGIApp(
    #    socketio_server=sio, socketio_path="socket.io"
    #)
    s = SocketIO()
    @s.sio.event
    def connect(*args, **kwargs):
       logger.info('connected', args, kwargs)

    app.mount('/', s.asgi_app)

    """
    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
       await websocket.accept()
       while True:
           data = await websocket.receive_text()
           await websocket.send_text(f"Message text was: {data}")
    """
    return app


# app = get_app()

# sio = socketio.AsyncServer(async_mode='asgi')
# sio_asgi_app = socketio.ASGIApp(sio, app)
# app.mount("/api/socket.io", sio_asgi_app)

# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#    await websocket.accept()
#    while True:
#        data = await websocket.receive_text()
#        await websocket.send_text(f"Message text was: {data}")
