from typing import List

from fastapi import APIRouter, Depends, Security

from guarantor.db.dao.deal import DealDAO
from guarantor.db.models.api_client import ApiClient
from guarantor.db.models.deal import Deal
from guarantor.web.api.v1.deals.schema import (DealCreateSchema, DealResponseSchema,
                                               DealUpdateSchema)
from guarantor.web.auth import get_user_by_api_key
from guarantor.web.dependencies import valid_owned_deal

router = APIRouter()


@router.get("/", response_model=List[DealResponseSchema])
async def list_deals(
    api_client: ApiClient = Security(get_user_by_api_key),
    deal_dao: DealDAO = Depends(),
) -> List[Deal]:
    """
    Список сделок
    """
    return await deal_dao.filter({"api_client": api_client})


@router.post("/", response_model=DealResponseSchema)
async def create_deal(
    deal: DealCreateSchema,
    api_client: ApiClient = Security(get_user_by_api_key),
    deal_dao: DealDAO = Depends(),
) -> Deal:
    """
    Создание сделки
    """
    to_create = deal.dict(exclude_none=True)
    to_create.update({"api_client": api_client})
    return await deal_dao.create(to_create)


@router.get("/{deal_id}", response_model=DealResponseSchema)
async def get_deal(deal: Deal = Depends(valid_owned_deal)) -> Deal:
    return deal


@router.patch("/{deal_id}", response_model=DealResponseSchema)
async def update_deal(
    data: DealUpdateSchema,
    deal: Deal = Depends(valid_owned_deal),
    deal_dao: DealDAO = Depends(),
) -> Deal:
    """
    Partial update сделки
    """
    return await deal_dao.update(deal.id, data.dict(exclude_none=True))

