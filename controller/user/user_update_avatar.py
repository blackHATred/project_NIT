from sanic.request import Request
from sanic.response import text
import aiofiles
import imghdr

from sanic.exceptions import InvalidUsage, Forbidden
from model.Upload import Upload
from helpers.check_request import check_request
from config.configuration import UPLOAD_DIR, MAX_FILE_SIZE


async def user_update_avatar(request: Request, user_id: int):
    user = (await check_request(request, list(), True))[1]

    if user.id != user_id: raise Forbidden('You do not have permission to update this avatar')

    upload_file = request.files.get('photo')
    if not upload_file: raise InvalidUsage('You need to upload a photo')
    if len(upload_file.body) > MAX_FILE_SIZE: raise InvalidUsage(f'Photo size must be less than {MAX_FILE_SIZE} bytes')

    if imghdr.what(None, upload_file.body) == 'jpeg': file_type = 'jpg'
    elif imghdr.what(None, upload_file.body) == 'png': file_type = 'png'
    elif imghdr.what(None, upload_file.body) == 'gif': file_type = 'gif'
    else: raise InvalidUsage('Photo must be .jpg, .png or .gif')

    upload = await Upload.save_upload(user_id=user_id, file_type=file_type)
    async with aiofiles.open(f'{UPLOAD_DIR}\\{upload.id}.{file_type}', 'wb') as f:
        await f.write(upload_file.body)
    f.close()
    await user.update(photo=upload.id)

    return text('Success')
