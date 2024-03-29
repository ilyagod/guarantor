from typing import Awaitable, Callable

from fastapi import FastAPI


def register_startup_event(
    app: FastAPI,
) -> Callable[[], Awaitable[None]]:  # pragma: no cover
    """
    Actions to run on application startup.

    This function uses fastAPI app to store data
    inthe state, such as db_engine.

    :param app: the fastAPI application.
    :return: function that actually performs actions.
    """

    @app.on_event("startup")
    async def _startup() -> None:  # noqa: WPS430
        # await init_kafka(app)
        pass  # noqa: WPS420

    # @app.on_event("startup")
    # @repeat_every(seconds=60)
    # async def task_check_payments():
    #     await check_payments()

    return _startup


def register_shutdown_event(
    app: FastAPI,
) -> Callable[[], Awaitable[None]]:  # pragma: no cover
    """
    Actions to run on application's shutdown.

    :param app: fastAPI application.
    :return: function that actually performs actions.
    """

    @app.on_event("shutdown")
    async def _shutdown() -> None:  # noqa: WPS430
        # await shutdown_kafka(app)
        pass  # noqa: WPS420

    return _shutdown
