from tortoise import fields, models

from guarantor.enums import Currency, DealStatus


class Deal(models.Model):
    id = fields.IntField(pk=True)

    title = fields.CharField(max_length=128)
    description = fields.TextField()

    api_client = fields.ForeignKeyField("models.ApiClient")
    price = fields.DecimalField(12, 2)
    currency = fields.CharEnumField(Currency, default=Currency.RUB)
    status = fields.CharEnumField(DealStatus, default=DealStatus.UNCONFIRMED)

    customer_id = fields.IntField()
    performer_id = fields.IntField()

    deadline_at = fields.DatetimeField(default=None, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "deals"
