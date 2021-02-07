from tortoise.exceptions import DoesNotExist
from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator

from sanic.exceptions import NotFound, InvalidUsage


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
    async def find(msg_id: int, is_deleted: bool = False, **kwargs):
        try:
            return await Msg.get(id=msg_id, is_deleted=is_deleted, **kwargs)
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

    async def dump(self):
        msg = (await MsgSchema.from_tortoise_orm(self)).dict()
        msg['created_at'] = str(msg['created_at'])
        msg['updated_at'] = str(msg['updated_at'])
        return msg

    def __str__(self):
        return self.message


MsgSchema = pydantic_model_creator(Msg)
