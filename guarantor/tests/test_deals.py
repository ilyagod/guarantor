from typing import Any, Dict

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from starlette import status

from guarantor.enums import DealStatus, DisputeStatus


@pytest.mark.anyio
async def test_deals(
    client: AsyncClient,
    fastapi_app: FastAPI,
    test_deal_1: Dict[str, Any],
) -> None:
    # Test empty deal list
    url = fastapi_app.url_path_for("list_deals")
    response = await client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []

    # test create deal
    url = fastapi_app.url_path_for("create_deal")
    response = await client.post(url, json=test_deal_1)
    assert response.status_code == status.HTTP_200_OK

    # test get deal
    url = fastapi_app.url_path_for("get_deal", deal_id=1)
    response = await client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == test_deal_1["title"]

    # test create dispute when deal in bad status
    url = fastapi_app.url_path_for("create_dispute", deal_id=1)
    response = await client.post(url, json={"title": "test", "description": "test"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # test update deal
    url = fastapi_app.url_path_for("update_deal", deal_id=1)

    response = await client.patch(url, json={"status": DealStatus.CONFIRMED})
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == DealStatus.CONFIRMED

    # test create dispute
    url = fastapi_app.url_path_for("create_dispute", deal_id=1)
    response = await client.post(url, json={"title": "test", "description": "test"})
    assert response.status_code == status.HTTP_200_OK

    # test update dispute
    url = fastapi_app.url_path_for("update_dispute", deal_id=1)
    response = await client.patch(url, json={"status": DisputeStatus.CLOSED_SUCCESS})
    assert response.status_code == status.HTTP_200_OK
    j = response.json()
    assert j["status"] == DealStatus.COMPLETED_AFTER_DISPUTE
    assert j["dispute"]["status"] == DisputeStatus.CLOSED_SUCCESS

    # test update closed dispute
    url = fastapi_app.url_path_for("update_dispute", deal_id=1)
    response = await client.patch(url, json={"status": DisputeStatus.CLOSED_SUCCESS})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
