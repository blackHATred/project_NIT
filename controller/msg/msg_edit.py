from sanic.request import Request
from sanic.response import json

from helpers.check_request import check_request
from helpers.auth_token import decode_auth_token
from model.User import User
from model.Msg import Msg
from tortoise.exceptions import DoesNotExist
from view.exceptions import InvalidUsage, Forbidden


async def msg_edit(request: Request, message_id: int):
    request = check_request(request, list('message'), True)

    try: user = await User.get(id=decode_auth_token(request.cookies.get('Authorization')), is_deleted=False)
    except DoesNotExist: raise InvalidUsage('You need to log in again')
    try: msg = await Msg.get(id=message_id, is_deleted=False)
    except DoesNotExist: raise InvalidUsage('This message does not exist')
    if msg.sender_id != user.id: raise Forbidden('You do not have permission to edit this message')

    msg.message = request.json.get('message')
    await msg.save()
    await msg.refresh_from_db()
    return json({
        'id': msg.id,
        'sender_id': msg.sender_id,
        'recipient_id': msg.recipient_id,
        'created_at': str(msg.created_at),
        'updated_at': str(msg.updated_at),
        'message': msg.message
    })