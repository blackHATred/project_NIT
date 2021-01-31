from sanic.request import Request
from sanic.response import json

from model.User import User


async def user_info(request: Request, user_id: int):
    user = await User.find(user_id=user_id, is_deleted=False)

    return json({
        'login': user.login,
        'created_at': str(user.created_at),
        'updated_at': str(user.updated_at),
        'first_name': user.first_name,
        'last_name': user.last_name
    })
