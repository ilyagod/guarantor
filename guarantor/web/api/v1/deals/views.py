from typing import List

from fastapi import APIRouter, Depends, Security

from guarantor.db.dao.deal import DealDAO
from guarantor.db.models.api_client import ApiClient
from guarantor.db.models.deal import Deal
from guarantor.web.api.v1.deals.schema import DealIncoming, DealOutgoing
from guarantor.web.auth import get_user_by_api_key

router = APIRouter()


@router.get("/", response_model=List[DealOutgoing])
async def list_deals(
    api_client: ApiClient = Security(get_user_by_api_key),
    deal_dao: DealDAO = Depends(),
) -> List[Deal]:
    """
    Список сделок
    """
    return await deal_dao.filter({'api_client': api_client})


@router.post("/", response_model=DealOutgoing)
async def create_deal(
    deal: DealIncoming,
    api_client: ApiClient = Security(get_user_by_api_key),
    deal_dao: DealDAO = Depends(),
) -> Deal:
    """
    Создание сделки
    """
    to_create = deal.dict(exclude_none=True)
    to_create.update({'api_client': api_client})
    return await deal_dao.create(to_create)
