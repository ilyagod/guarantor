from typing import Any, Dict, List, Optional

from fastapi import Depends, Security
from loguru import logger
from tortoise import transactions

from guarantor.constants import (
    DEAL_CREATE_DISPUTE_ALLOWED,
    DISPUTE_TO_DEAL_STATUS_MAPPING,
    DISPUTE_UPDATE_STATUS_ALLOWED,
)
from guarantor.db.dao.deal import DealDAO
from guarantor.db.dao.dispute import DisputeDAO
from guarantor.db.models.api_client import ApiClient
from guarantor.db.models.deal import Deal
from guarantor.enums import DealStatus
from guarantor.services.deal.exceptions import (
    DealNotFoundException,
    DisputeAlreadyCreated,
    DisputeCreateNotAllowed,
    DisputeDoesNotExists,
    DisputeUpdateNotAllowed,
)
from guarantor.web.auth import get_user_by_api_key


async def dependency_get_deal(
    api_client: ApiClient = Security(get_user_by_api_key),
    deal_id: Optional[int] = None,
) -> Optional[Deal]:
    deal = None
    if deal_id:
        deal = await DealDAO.get_or_none_with_prefetch(
            {"id": deal_id, "api_client": api_client},
            "dispute",
        )
        if not deal:
            raise DealNotFoundException
        logger.configure(extra={"deal_id": deal_id})
    return deal


class DealService:
    def __init__(
        self,
        api_client: ApiClient = Security(get_user_by_api_key),
        deal: Optional[Deal] = Depends(dependency_get_deal),
    ) -> None:
        self.api_client = api_client
        self._deal = deal

    async def create_deal(self, data: Dict[str, Any]) -> Deal:
        data.update({"api_client": self.api_client})
        deal = await DealDAO.create(data)
        return await self._get_deal(deal.id)

    async def get_all_deals(self) -> List[Deal]:
        return await DealDAO.filter_with_prefetch(
            {"api_client": self.api_client},
            "dispute",
        )

    def get_deal(self) -> Deal:
        return self._deal

    async def update_deal(self, data: Dict[str, Any]) -> Deal:
        return await DealDAO.update(self._deal.id, data, "dispute")

    async def create_dispute(self, data: Dict[str, Any]) -> Deal:
        if self._deal.status not in DEAL_CREATE_DISPUTE_ALLOWED:
            raise DisputeCreateNotAllowed

        if self._deal.dispute:
            raise DisputeAlreadyCreated

        data.update({"deal_id": self._deal.id})
        await DisputeDAO.create(data)

        return await DealDAO.update(
            self._deal.id,
            {"status": DealStatus.DISPUTE_OPENED},
            "dispute",
        )

    async def update_dispute(self, data: Dict[str, Any]) -> Deal:
        if not self._deal.dispute:
            raise DisputeDoesNotExists

        if self._deal.dispute.status not in DISPUTE_UPDATE_STATUS_ALLOWED:
            raise DisputeUpdateNotAllowed

        async with transactions.in_transaction():
            await DisputeDAO.update(self._deal.dispute.id, data)
            if (
                data.get("status")
                and data.get("status") in DISPUTE_TO_DEAL_STATUS_MAPPING
            ):
                return await DealDAO.update(
                    self._deal.id,
                    {
                        "status": DISPUTE_TO_DEAL_STATUS_MAPPING[data["status"]],
                    },
                    "dispute",
                )
            return await DealDAO.get_by_id(self._deal.id, "dispute")

    async def _get_deal(self, deal_id: int) -> Deal:
        deal = await DealDAO.get_or_none_with_prefetch(
            {"id": deal_id, "api_client": self.api_client},
            "dispute",
        )
        if not deal:
            raise DealNotFoundException

        return deal
