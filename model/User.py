from tortoise.models import Model
from tortoise import fields


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

    def __str__(self):
        return self.login
