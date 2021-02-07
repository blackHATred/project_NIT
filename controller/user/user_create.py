from sanic.request import Request
from sanic.response import json

from model.User import User
from helpers.check_request import check_request


async def user_create(request: Request):
    request = await check_request(request, ('login', 'password', 'first_name', 'last_name'))
    user = await User.register(**request)

    return json(await user.dump())


