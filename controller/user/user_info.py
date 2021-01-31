from sanic.request import Request
from sanic.response import json
from tortoise.exceptions import DoesNotExist

from model.User import User
from view.exceptions import InvalidUsage


async def user_info(request: Request, user_id: int):
    try:
        us = await User.get(id=user_id, is_deleted=False)
        return json({
            'login': us.login,
            'created_at': str(us.created_at),
            'updated_at': str(us.updated_at),
            'first_name': us.first_name,
            'last_name': us.last_name
        })
    except DoesNotExist:
        raise InvalidUsage('This user does not exist')
