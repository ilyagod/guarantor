from __future__ import annotations

from typing import TYPE_CHECKING

from tortoise import fields, models

from guarantor.enums import Currency

if TYPE_CHECKING:
    from guarantor.db.models.user import User


class UserCorrect(models.Model):
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField("models.User")
    amount = fields.DecimalField(12, 2)
    currency = fields.CharEnumField(Currency)

    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "user_corrects"
