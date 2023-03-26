from typing import List

from guarantor.db.dao.base import BaseDAO
from guarantor.db.models.deal import Deal
from guarantor.enums import DealStatus


class DealDAO(BaseDAO[Deal]):
    _model = Deal

    @classmethod
    async def get_waiting_for_payment_deals(cls, user_id: int) -> List[Deal]:
        return await cls.filter(
            {"user_id": user_id, "status": DealStatus.WAITING_FOR_PAYMENT},
        )
