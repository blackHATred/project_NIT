from tortoise.exceptions import DoesNotExist
from tortoise.models import Model
from tortoise import fields

from view.exceptions import InvalidUsage


class Token(Model):
    id = fields.BigIntField(pk=True)
    user_id = fields.IntField()

    @staticmethod
    async def check_valid(token_id: int, user_id: int):
        try:
            token = await Token.get(id=token_id)
            if token.user_id == user_id: return True
            else: raise InvalidUsage('Your session is invalid. Please log in again')
        except DoesNotExist:
            raise InvalidUsage('Your session is invalid. Please log in again')

    @staticmethod
    async def set_invalid(user_id: int):
        tokens = await Token.filter(user_id=user_id)
        for i in tokens:
            await i.delete()

    @staticmethod
    async def add(user_id: int):
        return await Token.create(user_id=user_id)

    def __str__(self):
        return f'{self.id} - {self.user_id}'
