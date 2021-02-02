from tortoise.exceptions import DoesNotExist, IntegrityError
from tortoise.models import Model
from tortoise import fields

from helpers.hash import hash_pass
from view.exceptions import InvalidUsage
import pyotp


class User(Model):
    id = fields.IntField(pk=True)
    login = fields.CharField(max_length=255, unique=True)
    hashed_password = fields.BinaryField()
    first_name = fields.CharField(max_length=255)
    last_name = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    is_deleted = fields.BooleanField(default=False)
    photo = fields.IntField(null=True, default=None)  # Альтернатива - ForeignKey для модели Upload
    totp_active = fields.BooleanField(default=False)
    totp_key = fields.CharField(max_length=26, null=True, default=None)

    @staticmethod
    async def find(user_id: int = None, user_login: str = None, **kwargs):
        try:
            if user_id is not None:
                return await User.get(id=user_id, **kwargs)
            elif user_login is not None:
                return await User.get(login=user_login, **kwargs)
        except DoesNotExist:
            raise InvalidUsage('This user does not exist')

    @staticmethod
    async def register(first_name: str, last_name: str, login: str, password: str):
        try:
            return await User.create(first_name=first_name,
                                     last_name=last_name,
                                     login=login,
                                     hashed_password=hash_pass(password))
        except IntegrityError:
            raise InvalidUsage('This login is already taken')

    async def update(self, **kwargs):
        try:
            await self.update_from_dict(kwargs)
            await self.save()
        except ValueError:
            raise InvalidUsage('Invalid data')

    async def add_totp(self):
        self.totp_key = pyotp.random_base32()
        await self.save()

    async def check_totp(self, code: str):
        if self.totp_key is None:
            raise InvalidUsage('Two-factor authentication not activated')
        if pyotp.TOTP(self.totp_key).verify(code):
            return True
        else:
            raise InvalidUsage('Code is invalid')

    def __str__(self):
        return self.login
