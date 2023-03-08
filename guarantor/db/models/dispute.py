from tortoise import fields, models


class Dispute(models.Model):
    dispute_id = fields.IntField(pk=True)

    deal = fields.OneToOneField("models.Deal", related_name="dispute")

    title = fields.CharField(max_length=128)
    description = fields.TextField()

    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "disputes"
