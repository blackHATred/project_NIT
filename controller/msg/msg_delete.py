from sanic.request import Request
from sanic.response import text

from helpers.check_request import check_request
from model.Msg import Msg
from view.exceptions import Forbidden


async def msg_delete(request: Request, message_id: int):
    request, user = await check_request(request, list(), True)
    msg = await Msg.find(msg_id=message_id, is_deleted=False)
    if msg.sender_id != user.id: raise Forbidden('You do not have permission to delete this message')

    await msg.update(is_deleted=True)
    return text('Success')
