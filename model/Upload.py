from tortoise.exceptions import DoesNotExist
from tortoise.models import Model
from tortoise import fields

from view.exceptions import NotFound


class Upload(Model):
    id = fields.IntField(pk=True)
    user_id = fields.IntField()  # Альтернатива - ForeignKey
    type = fields.CharField(max_length=3)

    @staticmethod
    async def save_upload(user_id: int, file_type: str):
        return await Upload.create(user_id=user_id, type=file_type)

    @staticmethod
    async def find(upload_id: int):
        try:
            return await Upload.get(id=upload_id)
        except DoesNotExist:
            raise NotFound('This message does not exist')

    def __str__(self):
        return self.id
