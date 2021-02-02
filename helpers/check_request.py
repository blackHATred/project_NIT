from typing import Union, Iterable

from sanic.request import Request

from helpers.auth_token import decode_auth_token
from model.Token import Token
from view.exceptions import InvalidUsage, Unauthorized
from model.User import User


async def check_request(request: Request, data: Union[Iterable, str], need_auth: bool = False):
    """
    Проверка на содержание data в request и валидация на соответствие типу string

    :param need_auth: если True, то проверяется наличие токена в куках
    :param request: request пользователя
    :param data: Данные, которые должны быть в реквесте
    :return: Exception или Request (+ User)
    """
    for i in data:
        if i not in request.json.keys():
            raise InvalidUsage(f'{i} info is missing')
        if request.json.get(i) is not str:
            try:
                request.json[i] = str(request.json[i])
            except AttributeError:
                raise InvalidUsage(f'{i} must be string')
    if need_auth:
        if request.cookies.get('Authorization') is None:
            raise Unauthorized('You need to be authorized')
        user_id, token = decode_auth_token(request.cookies.get('Authorization'))
        user = await User.find(user_id=user_id, is_deleted=False)
        valid = await Token.check_valid(token, user.id)
        if valid:
            return request, user

    return request
