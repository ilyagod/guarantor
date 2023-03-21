from typing import List

from guarantor.db.dao.base import BaseDAO
from guarantor.db.models.payment import Payment
from guarantor.enums import PaymentStatus


class PaymentDAO(BaseDAO[Payment]):
    _model = Payment

    @classmethod
    async def get_payments_for_check(cls) -> List[Payment]:
        return await cls.filter({"status": PaymentStatus.WAITING})
