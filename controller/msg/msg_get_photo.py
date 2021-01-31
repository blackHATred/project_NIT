from sanic.request import Request
from sanic.response import file

from config.configuration import UPLOAD_DIR
from helpers.check_request import check_request
from model.Msg import Msg
from model.Upload import Upload
from view.exceptions import InvalidUsage, Forbidden, NotFound


async def msg_get_photo(request: Request, message_id: int):
    request, user = await check_request(request, list(), True)
    msg = await Msg.find(msg_id=message_id, is_deleted=False)

    if user.id not in (msg.sender_id, msg.recipient_id):
        raise Forbidden('You do not have permission to view this photo')
    if msg.upload_id is not None:
        try:
            photo = await Upload.find(upload_id=msg.upload_id)
            return await file(f'{UPLOAD_DIR}\\{photo.id}.{photo.type}')
        except FileNotFoundError:
            raise NotFound('This photo was not found')
    else:
        raise InvalidUsage('No photo attached to this message')
