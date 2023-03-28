from datetime import datetime
from typing import Optional

from tortoise.transactions import in_transaction

from guarantor.constants import DEAL_UPDATE_STATUS_RULE, DISPUTE_CREATE_STATUS_ALLOWED
from guarantor.db.dao.deal_dao import DealDAO
from guarantor.db.dao.dispute_dao import DisputeDAO
from guarantor.db.dao.user_correct_dao import UserCorrectDAO
from guarantor.db.dao.user_dao import UserDAO
from guarantor.db.models.deal import Deal
from guarantor.enums import Currency, DealStatus
from guarantor.services.deal.exceptions import (
    CustomerUserNotFound,
    DealStatusChangeNotAllowed,
    DisputeAlreadyCreated,
    DisputeCreateNotAllowed,
    DisputeDoesNotExists,
    PerformerUserNotFound,
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
            },
        )

    async def confirm_deal(self, deal_id: int) -> Deal:
        deal = await DealDAO.get_by_id(deal_id)
        balances = await UserCorrectDAO.get_balances_dict(deal.customer.id)
        if balances.get(deal.currency, 0) >= deal.price:
            await UserCorrectDAO.create_correct(
                deal.customer.id,
                deal.price,
                deal.currency,
            )
            new_status = DealStatus.CONFIRM_PERFORMER
        else:
            new_status = DealStatus.WAITING_FOR_PAYMENT
        return await self._update_status(deal, new_status)

    async def deny_deal(self, deal_id: int) -> Deal:
        deal = await DealDAO.get_by_id(deal_id)
        return await self._update_status(deal, DealStatus.DENY_PERFORMER)

    async def create_dispute(self, deal_id: int, title: str, description: str) -> Deal:
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
            },
        )
        await deal.refresh_from_db()
        return deal

    async def close_performer(self, deal_id: int) -> Deal:
        return await self._close_dispute(deal_id, DealStatus.ARB_CLOSE_PERFORMER)

    async def close_customer(self, deal_id: int) -> Deal:
        return await self._close_dispute(deal_id, DealStatus.ARB_CLOSE_CUSTOMER)

    async def close(self, deal_id: int) -> Deal:
        deal = await DealDAO.get_by_id(deal_id)
        async with in_transaction():
            async with in_transaction():
                await UserCorrectDAO.create_correct(
                    deal.performer.id,
                    deal.price,
                    deal.currency,
                )
            return await self._update_status(deal, DealStatus.CLOSE)

    async def _close_dispute(self, deal_id: int, status: DealStatus) -> Deal:
        deal = await DealDAO.get_by_id(deal_id)
        if not deal.dispute:
            raise DisputeDoesNotExists
        async with in_transaction():
            user_id = (
                deal.customer.id
                if status == DealStatus.ARB_CLOSE_CUSTOMER
                else deal.performer.id
            )
            await UserCorrectDAO.create_correct(
                user_id,
                deal.price,
                deal.currency,
            )
            return await DealDAO.update(deal_id, {"status": status})

    async def _update_status(self, deal: Deal, to_status: DealStatus) -> Deal:
        if not self._status_change_allowed(deal.status, to_status):
            raise DealStatusChangeNotAllowed(deal.status, to_status)
        return await DealDAO.update(deal.id, {"status": to_status})

    def _status_change_allowed(
        self,
        from_status: DealStatus,
        to_status: DealStatus,
    ) -> bool:
        return (
            from_status in DEAL_UPDATE_STATUS_RULE
            and to_status in DEAL_UPDATE_STATUS_RULE[from_status]
        )
