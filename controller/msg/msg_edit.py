from sanic.request import Request
from sanic.response import json

from helpers.check_request import check_request
from model.Msg import Msg
from sanic.exceptions import Forbidden


async def msg_edit(request: Request, message_id: int):
    request, user = await check_request(request, ['message'], True)
    msg = await Msg.find(msg_id=message_id)

    if msg.sender_id != user.id: raise Forbidden('You do not have permission to edit this message')

    await msg.update(message=request.json.get('message'))
    return json(await msg.dump())
