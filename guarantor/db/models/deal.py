from __future__ import annotations

import typing

from tortoise import fields, models

from guarantor.enums import Currency, DealStatus, DealType

if typing.TYPE_CHECKING:
    from guarantor.db.models.dispute import Dispute
    from guarantor.db.models.user import User


class Deal(models.Model):
    id = fields.IntField(pk=True)

    title = fields.CharField(max_length=128)
    description = fields.TextField()

    price = fields.DecimalField(12, 2)
    currency = fields.CharEnumField(Currency, default=Currency.RUB)
    status = fields.CharEnumField(DealStatus, default=DealStatus.CREATED)
    deal_type = fields.CharEnumField(DealType, default=DealType.COMMON)

    # chat_id = fields.UUIDField(default=uuid.uuid4)

    customer: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User",
        related_name="deals_as_customer",
    )
    performer: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User",
        related_name="deals_as_performer",
    )

    deadline_at = fields.DatetimeField(default=None, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    dispute: fields.ReverseRelation[Dispute]

    class Meta:
        table = "deals"
