from sanic.request import Request
from sanic.response import json

from model.User import User
from helpers.hash import check_pass
from helpers.auth_token import encode_auth_token
from helpers.check_request import check_request


async def user_auth(request: Request):
    request = check_request(request, ('login', 'password'))
    user = await User.find(user_login=request.json.get('login'), is_deleted=False)

    check_pass(request.json.get('password'), user.hashed_password)
    token = encode_auth_token(user.id)
    response = json({'Authorization': token})
    response.cookies['Authorization'] = token
    return response



