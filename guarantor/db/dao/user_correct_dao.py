from tortoise.functions import Sum

from guarantor.db.dao.base import BaseDAO
from guarantor.db.models.user_correct import UserCorrect
from guarantor.enums import Currency


class UserCorrectDAO(BaseDAO[UserCorrect]):
    _model = UserCorrect

    @classmethod
    async def get_balances(cls, user_id: int):
        balances = {x.value: 0 for x in Currency}
        result = (
            await cls._model.filter(user_id=user_id)
            .group_by("user_id", "currency")
            .annotate(balance=Sum("amount"))
            .values("balance", "currency")
        )
        for balance in result:
            balances.update({balance["currency"]: balance["balance"]})

        return [{"currency": x, "balance": y} for x, y in balances.items()]
