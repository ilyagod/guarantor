from datetime import datetime
from typing import Optional

from guarantor.constants import DEAL_UPDATE_STATUS_RULE, DISPUTE_CREATE_STATUS_ALLOWED
from guarantor.db.dao.deal import DealDAO
from guarantor.db.dao.dispute import DisputeDAO
from guarantor.db.dao.user_dao import UserDAO
from guarantor.db.models.deal import Deal
from guarantor.enums import Currency, DealStatus
from guarantor.services.deal.exceptions import (
    CustomerUserNotFound,
    DealStatusChangeNotAllowed,
    DisputeAlreadyCreated,
    DisputeCreateNotAllowed,
    PerformerUserNotFound, DisputeDoesNotExists,
)


class DealService:
    async def create_deal(
        self,
        title: str,
        description: str,
        price: float,
        currency: Currency,
        customer_id: int,
        performer_id: int,
        deadline_at: Optional[datetime] = None,
    ) -> Deal:

        for id_, exc in {
            customer_id: CustomerUserNotFound,
            performer_id: PerformerUserNotFound,
        }.items():
            if not await UserDAO.get_or_none({"id": id_}):
                raise exc

        return await DealDAO.create(
            {
                "title": title,
                "description": description,
                "price": price,
                "currency": currency,
                "customer_id": customer_id,
                "performer_id": performer_id,
                "deadline_at": deadline_at,
            }
        )

    async def confirm_deal(self, deal_id: int) -> Deal:
        deal = await DealDAO.get_by_id(deal_id)
        return await self._update_status(deal, DealStatus.CONFIRM_PERFORMER)

    async def deny_deal(self, deal_id: int) -> Deal:
        deal = await DealDAO.get_by_id(deal_id)
        return await self._update_status(deal, DealStatus.DENY_PERFORMER)

    async def create_dispute(self, deal_id: int, title: str, description: str):
        deal = await DealDAO.get_by_id(deal_id, "dispute")
        if deal.dispute:
            raise DisputeAlreadyCreated
        if deal.status not in DISPUTE_CREATE_STATUS_ALLOWED:
            raise DisputeCreateNotAllowed(deal.status)

        await DisputeDAO.create(
            {
                "title": title,
                "description": description,
                "deal_id": deal_id,
            }
        )
        await deal.refresh_from_db()
        return deal

    async def close_performer(self, deal_id: int):
        return await self._close_dispute(deal_id, DealStatus.ARB_CLOSE_PERFORMER)

    async def close_customer(self, deal_id: int):
        return await self._close_dispute(deal_id, DealStatus.ARB_CLOSE_CUSTOMER)

    async def _close_dispute(self, deal_id, status: DealStatus):
        deal = await DealDAO.get_by_id(deal_id)
        if not deal.dispute:
            raise DisputeDoesNotExists

        return await DealDAO.update(deal_id, {"status": status})

    async def _update_status(self, deal: Deal, to_status: DealStatus):
        if not self._status_change_allowed(deal.status, to_status):
            raise DealStatusChangeNotAllowed(deal.status, to_status)
        return await DealDAO.update(deal.id, {"status": to_status})

    def _status_change_allowed(self, from_status, to_status):
        return (
            from_status in DEAL_UPDATE_STATUS_RULE
            and to_status in DEAL_UPDATE_STATUS_RULE[from_status]
        )


"""
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
"""
