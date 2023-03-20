from __future__ import annotations

from typing import TYPE_CHECKING

from tortoise import fields, models

from guarantor.enums import TronWalletStatus

if TYPE_CHECKING:
    from guarantor.db.models.payment import Payment


class TronWallet(models.Model):
    wallet_id = fields.IntField(pk=True)
    address = fields.TextField()
    private_key = fields.TextField()
    public_key = fields.TextField()
    status = fields.CharEnumField(TronWalletStatus, default=TronWalletStatus.WAITING)
    amount = fields.DecimalField(12, 2)

    payment: fields.OneToOneRelation[Payment] = fields.OneToOneField(
        "models.Payment",
    )

    class Meta:
        table = "tron_wallets"
