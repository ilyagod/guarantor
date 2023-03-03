from tortoise import fields, models

from guarantor.enums import DisputeStatus


class Dispute(models.Model):
    id = fields.IntField(pk=True)

    deal = fields.OneToOneField('models.Deal', related_name='dispute')

    title = fields.CharField(max_length=128)
    description = fields.TextField()

    status = fields.CharEnumField(DisputeStatus, default=DisputeStatus.OPEN)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = 'disputes'
