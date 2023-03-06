import uuid
from typing import Any, AsyncGenerator, Dict
from unittest.mock import Mock

import nest_asyncio
import pytest
from aiokafka import AIOKafkaProducer
from fastapi import FastAPI
from httpx import AsyncClient
from tortoise import Tortoise
from tortoise.contrib.test import finalizer, initializer

from guarantor.db.config import MODELS_MODULES, TORTOISE_CONFIG
from guarantor.db.dao.api_client import ApiClientDAO
from guarantor.services.kafka.dependencies import get_kafka_producer
from guarantor.services.kafka.lifetime import init_kafka, shutdown_kafka
from guarantor.settings import settings
from guarantor.web.application import get_app

nest_asyncio.apply()


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    """
    Backend for anyio pytest plugin.

    :return: backend name.
    """
    return "asyncio"


@pytest.fixture(autouse=True)
async def initialize_db() -> AsyncGenerator[None, None]:
    """
    Initialize models and database.

    :yields: Nothing.
    """
    initializer(
        MODELS_MODULES,
        db_url=str(settings.db_url),
        app_label="models",
    )
    await Tortoise.init(config=TORTOISE_CONFIG)

    yield

    await Tortoise.close_connections()
    finalizer()


@pytest.fixture
async def test_kafka_producer() -> AsyncGenerator[AIOKafkaProducer, None]:
    """
    Creates kafka's producer.

    :yields: kafka's producer.
    """
    app_mock = Mock()
    await init_kafka(app_mock)
    yield app_mock.state.kafka_producer
    await shutdown_kafka(app_mock)


@pytest.fixture
def fastapi_app(
    test_kafka_producer: AIOKafkaProducer,
) -> FastAPI:
    """
    Fixture for creating FastAPI app.

    :return: fastapi app with mocked dependencies.
    """
    application = get_app()
    application.dependency_overrides[get_kafka_producer] = lambda: test_kafka_producer
    return application  # noqa: WPS331


@pytest.fixture
async def client(
    fastapi_app: FastAPI,
    anyio_backend: Any,
) -> AsyncGenerator[AsyncClient, None]:
    """
    Fixture that creates client for requesting server.

    :param fastapi_app: the application.
    :yield: client for the app.
    """

    obj = await ApiClientDAO.create(
        {
            "name": "test",
            "token": uuid.uuid4(),
        },
    )
    async with AsyncClient(
        app=fastapi_app,
        base_url="http://test",
        headers={"api_key": str(obj.token)},
    ) as ac:
        yield ac


@pytest.fixture
def test_deal_1() -> Dict[str, Any]:
    return {
        "title": "test",
        "description": "test",
        "price": 10,
        "customer_id": 1,
        "performer_id": 2,
    }
