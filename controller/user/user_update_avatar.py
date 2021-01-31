from sanic.request import Request
from sanic.response import text
import aiofiles
import imghdr
from tortoise.exceptions import DoesNotExist

from view.exceptions import InvalidUsage, Forbidden
from model.User import User
from model.Upload import Upload
from helpers.auth_token import decode_auth_token
from helpers.check_request import check_request
from config.configuration import UPLOAD_DIR, MAX_FILE_SIZE


async def user_update_avatar(request: Request, user_id: int):
    request = check_request(request, list(), True)
    try: user = await User.get(id=decode_auth_token(request.cookies.get('Authorization')), is_deleted=False)
    except DoesNotExist: raise InvalidUsage('You need to log in again')

    if user.id != user_id: raise Forbidden('You do not have permission to update this avatar')

    upload_file = request.files.get('photo')
    if not upload_file: raise InvalidUsage('You need to upload a photo')
    if len(upload_file.body) > MAX_FILE_SIZE: raise InvalidUsage(f'Photo size must be less than {MAX_FILE_SIZE} bytes')

    if imghdr.what(None, upload_file.body) == 'jpeg': file_type = 'jpg'
    elif imghdr.what(None, upload_file.body) == 'png': file_type = 'png'
    elif imghdr.what(None, upload_file.body) == 'gif': file_type = 'gif'
    else: raise InvalidUsage('Photo must be .jpg, .png or .gif')

    upload = await Upload.create(user_id=user_id, type=file_type)
    user.photo = upload.id
    await user.save()
    async with aiofiles.open(f'{UPLOAD_DIR}\\{upload.id}.{file_type}', 'wb') as f:
        await f.write(upload_file.body)
    f.close()
    return text('Success')
