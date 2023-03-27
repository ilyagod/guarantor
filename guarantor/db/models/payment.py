from __future__ import annotations

from typing import TYPE_CHECKING

from tortoise import fields, models

from guarantor.enums import Currency, PaymentStatus

if TYPE_CHECKING:
    from guarantor.db.models.payment_gateway import PaymentGateway
    from guarantor.db.models.user import User


class Payment(models.Model):
    id = fields.IntField(pk=True)
    gateway: fields.ForeignKeyRelation[PaymentGateway] = fields.ForeignKeyField(
        "models.PaymentGateway",
        related_name="payments",
    )
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User",
        related_name="payments",
    )
    status = fields.CharEnumField(PaymentStatus, default=PaymentStatus.WAITING)
    currency = fields.CharEnumField(Currency)
    amount = fields.DecimalField(12, 2)
    withdraw = fields.BooleanField(default=False, null=True)
    data = fields.JSONField(default={}, null=True)

    class Meta:
        table = "payments"
