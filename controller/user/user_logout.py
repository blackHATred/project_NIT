from sanic.request import Request
from sanic.response import text

from model.Token import Token
from helpers.check_request import check_request


async def user_logout(request: Request):
    # Пользователь выходит из аккаунта со всех устройств, поэтому все токены признаются недействительными
    request, user = await check_request(request, list(), True)
    await Token.set_invalid(user.id)

    response = text('Success')
    del request.cookies['Authorization']
    return response



