from __future__ import annotations

from typing import TYPE_CHECKING

from tortoise import fields, models

if TYPE_CHECKING:
    from guarantor.db.models.deal import Deal
    from guarantor.db.models.user import User


class ChatMessage(models.Model):
    id = fields.IntField(pk=True)
    deal: fields.ForeignKeyRelation[Deal] = fields.ForeignKeyField("models.Deal")
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField("models.User")

    message = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "chat_messages"
