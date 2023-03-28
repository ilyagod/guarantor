from __future__ import annotations

from typing import TYPE_CHECKING

from tortoise import fields, models

if TYPE_CHECKING:
    from guarantor.db.models.user import User


class TronWallet(models.Model):
    wallet_id = fields.IntField(pk=True)
    address = fields.TextField()
    private_key = fields.TextField()
    public_key = fields.TextField()

    user: fields.OneToOneRelation[User] = fields.OneToOneField(
        "models.User",
    )

    class Meta:
        table = "tron_wallets"
