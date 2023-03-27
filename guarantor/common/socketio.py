import socketio

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins=["*"])
asgi_app = socketio.ASGIApp(
    socketio_server=sio,
    socketio_path="socket.io",
)
