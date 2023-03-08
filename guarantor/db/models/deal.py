from tortoise import fields, models
from tortoise.fields import ReverseRelation

from guarantor.db.models.dispute import Dispute
from guarantor.db.models.user import User
from guarantor.enums import Currency, DealStatus, DealType


class Deal(models.Model):
    id = fields.IntField(pk=True)

    title = fields.CharField(max_length=128)
    description = fields.TextField()

    price = fields.DecimalField(12, 2)
    currency = fields.CharEnumField(Currency, default=Currency.RUB)
    status = fields.CharEnumField(DealStatus, default=DealStatus.CREATED)
    deal_type = fields.CharEnumField(DealType, default=DealType.COMMON)

    customer: fields.ForeignKeyRelation["User"] = fields.ForeignKeyField(
        "models.User", related_name="deals_as_customer"
    )
    performer: fields.ForeignKeyRelation["User"] = fields.ForeignKeyField(
        "models.User", related_name="deals_as_performer"
    )

    deadline_at = fields.DatetimeField(default=None, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    dispute: ReverseRelation["Dispute"]

    class Meta:
        table = "deals"

    class PydanticMeta:
        exclude_raw_fields = False
