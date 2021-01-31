from sanic.request import Request
from sanic.response import json

from model.User import User
from helpers.check_request import check_request


async def user_create(request: Request):
    request = check_request(request, ('login', 'password', 'first_name', 'last_name'))

    user = await User.register(request.json.get('first_name'),
                               request.json.get('last_name'),
                               request.json.get('login'),
                               request.json.get('password'))
    return json({
        'id': user.id,
        'login': user.login,
        'created_at': str(user.created_at),
        'updated_at': str(user.updated_at),
        'first_name': user.first_name,
        'last_name': user.last_name
    })


