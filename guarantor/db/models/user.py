from __future__ import annotations
from typing import TYPE_CHECKING

from tortoise import fields, models

if TYPE_CHECKING:
    from guarantor.db.models.tron_wallet import TronWallet


class User(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=64)
    external_id = fields.IntField()

    tron_wallet: fields.OneToOneRelation[TronWallet]

    class Meta:
        table = "users"
