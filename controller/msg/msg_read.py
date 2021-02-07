from sanic.request import Request
from sanic.response import json

from helpers.check_request import check_request
from model.Msg import Msg
from sanic.exceptions import Forbidden


async def msg_read(request: Request, message_id: int):
    request, user = await check_request(request, list(), True)
    msg = await Msg.find(msg_id=message_id, is_deleted=False)

    if user.id not in (msg.sender_id, msg.recipient_id):
        raise Forbidden('You do not have permission to view this message')
    return json(await msg.dump())
