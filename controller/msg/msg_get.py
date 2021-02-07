from sanic.request import Request
from sanic.response import json

from helpers.check_request import check_request
from model.Msg import Msg


async def msg_get(request: Request):
    request, user = await check_request(request, list(), True)

    # Учитываются не только принятые, но и отправленные сообщения
    outbox_messages = await Msg.list_find(sender_id=user.id)
    inbox_messages = await Msg.list_find(recipient_id=user.id)
    return json({
        'outbox_messages': [(await i.dump()) for i in outbox_messages],
        'inbox_messages': [(await i.dump()) for i in inbox_messages]
    })

