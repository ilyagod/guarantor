from typing import List

from fastapi import APIRouter, Depends, Security, HTTPException
from starlette import status
from tortoise import transactions

from guarantor.constants import (DEAL_CREATE_DISPUTE_ALLOWED,
                                 DISPUTE_UPDATE_STATUS_ALLOWED,
                                 DISPUTE_TO_DEAL_STATUS_MAPPING)
from guarantor.db.dao.deal import DealDAO
from guarantor.db.dao.dispute import DisputeDAO
from guarantor.db.models.api_client import ApiClient
from guarantor.db.models.deal import Deal
from guarantor.enums import DealStatus
from guarantor.web.api.v1.deals.schema import (
    DealCreateSchema,
    DealResponseSchema,
    DealUpdateSchema, DisputeCreateSchema, DisputeUpdateSchema,
)
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
    return await deal_dao.filter_with_prefetch({"api_client": api_client}, 'dispute')


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
    return await deal_dao.update(deal.id, data.dict(exclude_none=True), 'dispute')


@router.post("/{deal_id}/dispute", response_model=DealResponseSchema)
async def create_dispute(
    data: DisputeCreateSchema,
    deal: Deal = Depends(valid_owned_deal),
    dispute_dao: DisputeDAO = Depends(),
    deal_dao: DealDAO = Depends(),
):
    """
    Создание спора
    """
    if deal.status not in DEAL_CREATE_DISPUTE_ALLOWED:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            f"Спор можно создавать только для сделок со "
            f"статусами {*DEAL_CREATE_DISPUTE_ALLOWED,}",
        )
    if deal.dispute:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            f"Спор для данной сделки уже создан"
        )

    await dispute_dao.create({
        'title': data.title,
        'description': data.description,
        'deal_id': deal.id
    })
    deal = await deal_dao.update(deal.id, {'status': DealStatus.DISPUTE_OPENED}, 'dispute')

    return deal


@router.patch("/{deal_id}/dispute", response_model=DealResponseSchema)
async def create_dispute(
    data: DisputeUpdateSchema,
    deal: Deal = Depends(valid_owned_deal),
    dispute_dao: DisputeDAO = Depends(),
    deal_dao: DealDAO = Depends(),
):
    """Редактирование спора"""
    if not deal.dispute:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            f"Спор для данной сделки не существует"
        )

    if deal.dispute.status not in DISPUTE_UPDATE_STATUS_ALLOWED:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Можно редактировать только споры в "
            f"статусе: {*DISPUTE_UPDATE_STATUS_ALLOWED,}"
        )

    async with transactions.in_transaction():
        await dispute_dao.update(deal.dispute.id, data.dict(exclude_none=True))
        if data.status and data.status in DISPUTE_TO_DEAL_STATUS_MAPPING:
            deal = await deal_dao.update(deal.id, {
                'status': DISPUTE_TO_DEAL_STATUS_MAPPING[data.status]
            }, 'dispute')

    deal = deal_dao.get_by_id(deal)
    return deal
