from sanic.request import Request
from sanic.response import json
import imghdr
import aiofiles

from helpers.check_request import check_request
from model.User import User
from model.Msg import Msg
from model.Upload import Upload
from view.exceptions import InvalidUsage, Forbidden, Unauthorized
from config.configuration import MAX_FILE_SIZE, UPLOAD_DIR


async def msg_create(request: Request):
    if request.cookies.get('Authorization') is None: raise Unauthorized('You need to be authorized')
    if 'message' not in request.form.keys(): raise InvalidUsage('message info is missing')
    if 'recipient' not in request.form.keys(): raise InvalidUsage('recipient info is missing')

    request, user = await check_request(request, list(), True)
    recipient = await User.find(user_login=request.form.get('recipient'), is_deleted=False)

    if 'reply_id' in request.form:
        reply_msg = await Msg.find(msg_id=request.form.get('reply_id'))
        if user.id not in (reply_msg.recipient_id, reply_msg.sender_id):
            raise Forbidden('You have not permission to reply this message')
        reply_msg = reply_msg.id
    else:
        reply_msg = None

    # Добавление картинки к сообщению
    upload_file = request.files.get('photo')
    if upload_file:
        if MAX_FILE_SIZE < len(upload_file.body):
            raise InvalidUsage(f'Photo size must be less than {MAX_FILE_SIZE} bytes')
        if imghdr.what(None, upload_file.body) == 'jpeg': file_type = 'jpg'
        elif imghdr.what(None, upload_file.body) == 'png': file_type = 'png'
        elif imghdr.what(None, upload_file.body) == 'gif': file_type = 'gif'
        else: raise InvalidUsage('Photo must be .jpg, .png or .gif')

        upload = await Upload.save_upload(user_id=user.id, file_type=file_type)
        async with aiofiles.open(f'{UPLOAD_DIR}\\{upload.id}.{file_type}', 'wb') as f:
            await f.write(upload_file.body)
        f.close()
        msg = await Msg.send(message=request.form.get('message'),
                             recipient_id=recipient.id,
                             sender_id=user.id,
                             upload_id=upload.id,
                             reply_id=reply_msg)
    else:
        msg = await Msg.send(message=request.form.get('message'),
                             recipient_id=recipient.id,
                             sender_id=user.id,
                             reply_id=reply_msg)
    return json({
        'id': msg.id,
        'sender_id': msg.sender_id,
        'recipient_id': msg.recipient_id,
        'upload_id': msg.upload_id,
        'created_at': str(msg.created_at),
        'updated_at': str(msg.updated_at),
        'message': msg.message,
        'reply_id': msg.reply_id
    })
