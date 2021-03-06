from sanic.request import Request
from sanic.response import file

from model.User import User
from model.Upload import Upload
from config.configuration import UPLOAD_DIR


async def user_get_avatar(request: Request, user_id: int):
    user = await User.find(user_id=user_id)

    if user.photo is not None:
        try:
            photo = await Upload.get(id=user.photo)
            return await file(f'{UPLOAD_DIR}\\{photo.id}.{photo.type}')
        except FileNotFoundError:
            return await file('default_avatar.jpg')
    else:
        return await file('default_avatar.jpg')
