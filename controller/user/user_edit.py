from sanic.request import Request
from sanic.response import json
from tortoise.exceptions import DoesNotExist
# import datetime as dt

from helpers.check_request import check_request
from helpers.auth_token import decode_auth_token
from view.exceptions import Forbidden, Unauthorized, InvalidUsage
from model.User import User


async def user_edit(request: Request, user_id: int):
    request = check_request(request, ('first_name', 'last_name'), True)

    try: user_to_edit = await User.get(id=user_id, is_deleted=False)
    except DoesNotExist: raise InvalidUsage('This user does not exist')
    try: user = await User.get(id=decode_auth_token(request.cookies.get('Authorization')), is_deleted=False)
    except DoesNotExist: raise InvalidUsage('You need to log in again')

    if user_to_edit.id != user.id:
        raise Forbidden('You do not have permission for edit this user')

    user.first_name, user.last_name = request.json.get('first_name'), request.json.get('last_name')
    # время обновления менять не обязательно, ORM делает это автоматически
    # user.updated_at = dt.datetime.utcnow()
    await user.save()
    await user.refresh_from_db()
    return json({
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'login': user.login,
        'created_at': str(user.created_at),
        'updated_at': str(user.updated_at)
    })
