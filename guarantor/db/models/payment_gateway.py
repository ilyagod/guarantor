from tortoise import fields, models
from tortoise.contrib.postgres.fields import ArrayField


class PaymentGateway(models.Model):
    id = fields.IntField(pk=True)

    name = fields.CharField(max_length=128)
    logo = fields.TextField(default=None, null=True)
    currency = ArrayField(element_type="varchar")

    created_at = fields.DatetimeField(auto_now_add=True)
    python_service = fields.CharField(max_length=32)

    class Meta:
        table = "payment_gateways"
