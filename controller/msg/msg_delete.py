from sanic.request import Request
from sanic.response import text

from helpers.auth_token import decode_auth_token
from helpers.check_request import check_request
from model.User import User
from model.Msg import Msg
from tortoise.exceptions import DoesNotExist
from view.exceptions import InvalidUsage, Forbidden, NotFound


async def msg_delete(request: Request, message_id: int):
    request = check_request(request, list(), True)

    try: user = await User.get(id=decode_auth_token(request.cookies.get('Authorization')), is_deleted=False)
    except DoesNotExist: raise InvalidUsage('You need to log in again')
    try: msg = await Msg.get(id=message_id, is_deleted=False)
    except DoesNotExist: raise NotFound('This message does not exist')
    if msg.sender_id != user.id: raise Forbidden('You do not have permission to delete this message')

    msg.is_deleted = True
    await msg.save()
    return text('Success')
