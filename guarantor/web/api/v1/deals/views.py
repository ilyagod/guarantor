from typing import List

from fastapi import APIRouter, Depends, Security

from guarantor.db.dao.deal import DealDTO
from guarantor.db.models.api_client import ApiClient
from guarantor.db.models.deal import Deal
from guarantor.web.api.v1.deals.schema import DealIncoming, DealOutgoing
from guarantor.web.auth import get_user_by_api_key

router = APIRouter()


@router.get("/", response_model=List[DealOutgoing])
async def list_deals(
    api_client: ApiClient = Security(get_user_by_api_key),
    deal_dto: DealDTO = Depends(),
) -> List[Deal]:
    """
    Список сделок
    """
    return await deal_dto.get_all(api_client)


@router.post("/", response_model=DealOutgoing)
async def create_deal(
    deal: DealIncoming,
    api_client: ApiClient = Security(get_user_by_api_key),
    deal_dto: DealDTO = Depends(),
) -> Deal:
    """
    Создание сделки
    """
    return await deal_dto.create_deal(deal, api_client)
