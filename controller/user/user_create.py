from sanic.request import Request
from sanic.response import json
from tortoise.exceptions import IntegrityError

from view.exceptions import InvalidUsage
from model.User import User
from helpers.hash import hash_pass
from helpers.check_request import check_request


async def user_create(request: Request):
    request = check_request(request, ('login', 'password', 'first_name', 'last_name'))
    try:
        user = await User.create(first_name=request.json['first_name'],
                                 last_name=request.json['last_name'],
                                 login=request.json['login'],
                                 hashed_password=hash_pass(request.json['password']))
        return json({
            'id': user.id,
            'login': user.login,
            'created_at': str(user.created_at),
            'updated_at': str(user.updated_at),
            'first_name': user.first_name,
            'last_name': user.last_name
        })
    except IntegrityError:
        raise InvalidUsage('This login is already taken')


