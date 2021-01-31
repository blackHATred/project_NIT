from sanic.request import Request
from sanic.response import json
from tortoise.exceptions import DoesNotExist

from view.exceptions import InvalidUsage
from model.User import User
from helpers.hash import check_pass
from helpers.auth_token import encode_auth_token
from helpers.check_request import check_request


async def user_auth(request: Request):
    request = check_request(request, ('login', 'password'))
    try:
        user = await User.get(login=request.json.get('login'))
        if user.is_deleted: raise InvalidUsage('This user is deleted')
        check_pass(request.json.get('password'), user.hashed_password)
        token = encode_auth_token(user.id)
        response = json({'Authorization': token})
        response.cookies['Authorization'] = token
        return response
    except DoesNotExist:
        raise InvalidUsage('User with this login does not exist')


