import socketio
from loguru import logger


class SocketIO:
    instance = None

    def __new__(cls):
        if not cls.instance:
            logger.info("aaaaaa")
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        self.sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins=["*"])
        self.asgi_app = socketio.ASGIApp(
            socketio_server=self.sio, socketio_path="socket.io"
        )
