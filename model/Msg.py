from tortoise.exceptions import DoesNotExist
from tortoise.models import Model
from tortoise import fields

from view.exceptions import NotFound, InvalidUsage


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

    @staticmethod
    async def find(msg_id: int, **kwargs):
        try:
            return await Msg.get(id=msg_id, **kwargs)
        except DoesNotExist:
            raise NotFound('This message does not exist')

    @staticmethod
    async def send(message: str, recipient_id: int, sender_id: int, **kwargs):
        return await Msg.create(message=message, recipient_id=recipient_id, sender_id=sender_id, **kwargs)

    @staticmethod
    async def list_find(**kwargs):
        return await Msg.filter(**kwargs)

    async def update(self, **kwargs):
        try:
            await self.update_from_dict(kwargs)
            await self.save()
        except ValueError:
            raise InvalidUsage('Invalid data')

    def __str__(self):
        return self.message
