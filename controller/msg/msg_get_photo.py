from sanic.request import Request
from sanic.response import file
from tortoise.exceptions import DoesNotExist

from config.configuration import UPLOAD_DIR
from helpers.auth_token import decode_auth_token
from helpers.check_request import check_request
from model.Msg import Msg
from model.Upload import Upload
from model.User import User
from view.exceptions import InvalidUsage, Forbidden, NotFound


async def msg_get_photo(request: Request, message_id: int):
    request = check_request(request, list(), True)

    try: user = await User.get(id=decode_auth_token(request.cookies.get('Authorization')), is_deleted=False)
    except DoesNotExist: raise InvalidUsage('You need to log in again')

    try: msg = await Msg.get(id=message_id, is_deleted=False)
    except DoesNotExist: raise InvalidUsage('This message does not exist')

    if user.id not in (msg.sender_id, msg.recipient_id): raise Forbidden('You have not permission to view this photo')
    if msg.upload_id is not None:
        try:
            photo = await Upload.get(id=msg.upload_id)
            return await file(f'{UPLOAD_DIR}\\{photo.id}.{photo.type}')
        except FileNotFoundError:
            raise NotFound('This photo was not found')
    else:
        raise InvalidUsage('No photo attached to this message')
