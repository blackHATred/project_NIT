from typing import Union, Iterable

from sanic.request import Request
from view.exceptions import InvalidUsage, Unauthorized


def check_request(request: Request, data: Union[Iterable, str], need_auth: bool = False) -> Request:
    """
    Проверка на содержание data в request и валидация на соответствие типу string

    :param need_auth: если True, то проверяется наличие токена в куках
    :param request: request пользователя
    :param data: Данные, которые должны быть в реквесте
    :return: Exception или Request
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
    return request
