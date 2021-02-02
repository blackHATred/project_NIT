from sanic.request import Request
from sanic.response import json

from model.User import User
from model.Token import Token
from helpers.hash import check_pass
from helpers.auth_token import encode_auth_token
from helpers.check_request import check_request
from view.exceptions import InvalidUsage


async def user_auth(request: Request):
    request = await check_request(request, ('login', 'password'))
    user = await User.find(user_login=request.json.get('login'), is_deleted=False)

    await check_pass(request.json.get('password'), user.hashed_password)
    if user.totp_active:
        if '2FA_code' not in request.json.keys():
            raise InvalidUsage('2FA code is required')
        await user.check_totp(request.json.get('2FA_code'))

    token = await Token.add(user.id)
    token = encode_auth_token(user.id, token.id)
    response = json({'Authorization': token})
    response.cookies['Authorization'] = token
    return response



