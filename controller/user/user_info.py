from sanic.request import Request
from sanic.response import json

from model.User import User


async def user_info(request: Request, user_id: int):
    user = await User.find(user_id=user_id)

    return json(await user.dump())
