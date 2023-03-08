from tortoise import fields, models


class User(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=64)
    external_id = fields.IntField()

    class Meta:
        table = "users"

    class PydanticMeta:
        exclude_raw_fields = False
