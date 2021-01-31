from sanic.request import Request
from sanic.response import json

from helpers.check_request import check_request
from model.Msg import Msg


async def msg_get(request: Request):
    request, user = await check_request(request, list(), True)

    # Учитываются не только принятые, но и отправленные сообщения
    outbox_messages = await Msg.list_find(sender_id=user.id, is_deleted=False)
    inbox_messages = await Msg.list_find(recipient_id=user.id, is_deleted=False)
    return json({
        'outbox_messages': [
            {
                'id': i.id,
                'sender_id': i.sender_id,
                'recipient_id': i.recipient_id,
                'created_at': str(i.created_at),
                'updated_at': str(i.updated_at),
                'message': i.message,
                'upload_id': i.upload_id,
                'reply_id': i.reply_id
            } for i in outbox_messages
        ],
        'inbox_messages': [
            {
                'id': i.id,
                'sender_id': i.sender_id,
                'recipient_id': i.recipient_id,
                'created_at': str(i.created_at),
                'updated_at': str(i.updated_at),
                'message': i.message,
                'upload_id': i.upload_id,
                'reply_id': i.reply_id
            } for i in inbox_messages
        ]
    })

