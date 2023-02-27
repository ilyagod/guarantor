from tortoise import fields, models


class ApiClient(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=256)
    token = fields.UUIDField()
    is_active = fields.BooleanField(default=True)

    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "api_clients"
