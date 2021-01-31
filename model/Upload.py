from tortoise.models import Model
from tortoise import fields


class Upload(Model):
    id = fields.IntField(pk=True)
    user_id = fields.IntField()  # Альтернатива - ForeignKey
    type = fields.CharField(max_length=3)

    def __str__(self):
        return self.id
