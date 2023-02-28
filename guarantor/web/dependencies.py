from typing import Mapping

from fastapi import Depends, HTTPException, Security
from starlette.status import HTTP_404_NOT_FOUND

from guarantor.db.dao.deal import DealDAO
from guarantor.db.models.api_client import ApiClient
from guarantor.web.auth import get_user_by_api_key


async def valid_owned_deal(
    deal_id: int,
    api_client: ApiClient = Security(get_user_by_api_key),
    deal_dao: DealDAO = Depends(),
) -> Mapping:
    deal = await deal_dao.get_or_none(
        {
            "api_client": api_client,
            "id": deal_id,
        },
    )
    if not deal:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            "deal not found",
        )

    return deal
