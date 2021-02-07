from typing import Union, Iterable
from sanic.request import Request
from sanic.exceptions import *

from helpers.auth_token import decode_auth_token
from model.Token import Token
from model.User import User


async def check_request(request: Request, data: Union[Iterable, str], need_auth: bool = False):
    """
    Валидатор реквеста
    Проверка на содержание data в request и валидация на соответствие типу string

    :param need_auth: если True, то проверяется наличие токена в куках
    :param request: request пользователя
    :param data: Данные, которые должны быть в реквесте
    :return: Exception или Request (+ User)
    """
    for key in data:
        if key not in request.json.keys():
            raise InvalidUsage(f'{key} info is missing')
        if not isinstance(request.json.get(key), str):
            try:
                request.json[key] = str(request.json[key])
            except AttributeError:
                raise InvalidUsage(f'{key} must be string')

    if need_auth:
        if request.cookies.get('Authorization') is None:
            raise Unauthorized('You need to be authorized')
        user_id, token = decode_auth_token(request.cookies.get('Authorization'))
        try:
            user = await User.find(user_id=user_id)
        except User.DoesNotExist:
            raise InvalidUsage('This user does not exist')
        await Token.check_valid(token, user.id)
        try:
            return request.json, user
        except InvalidUsage:
            return user

    return request.json
