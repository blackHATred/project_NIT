from sanic.request import Request
from sanic.response import json
from tortoise.exceptions import DoesNotExist

from helpers.auth_token import decode_auth_token
from helpers.check_request import check_request
from model.User import User
from model.Msg import Msg
from view.exceptions import InvalidUsage


async def msg_get(request: Request):
    request = check_request(request, list(), True)

    try: user = await User.get(id=decode_auth_token(request.cookies.get('Authorization')), is_deleted=False)
    except DoesNotExist: raise InvalidUsage('You need to log in again')

    # Учитываются не только принятые, но и отправленные сообщения
    outbox_messages = await Msg.filter(sender_id=user.id, is_deleted=False)
    inbox_messages = await Msg.filter(recipient_id=user.id, is_deleted=False)
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

