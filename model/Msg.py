from tortoise.models import Model
from tortoise import fields


class Msg(Model):
    id = fields.IntField(pk=True)
    sender_id = fields.IntField()     # Альтернатива - ForeignKey
    recipient_id = fields.IntField()  # Альтернатива - ForeignKey
    message = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    is_deleted = fields.BooleanField(default=False)
    upload_id = fields.IntField(null=True, default=None)  # Альтернатива - ForeignKey
    reply_id = fields.IntField(null=True, default=None)   # Альтернатива - ForeignKey

    def __str__(self):
        return self.message
