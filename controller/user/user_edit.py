from sanic.request import Request
from sanic.response import json
# import datetime as dt

from helpers.check_request import check_request
from view.exceptions import Forbidden
from model.User import User


async def user_edit(request: Request, user_id: int):
    request, user = await check_request(request, ('first_name', 'last_name'), True)
    user_to_edit = await User.find(user_id=user_id, is_deleted=False)

    if user_to_edit.id != user.id:
        raise Forbidden('You do not have permission for edit this user')

    # время обновления менять не обязательно, ORM делает это автоматически
    # user.updated_at = dt.datetime.utcnow()
    await user.update(first_name=request.json.get('first_name'), last_name=request.json.get('last_name'))
    return json({
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'login': user.login,
        'created_at': str(user.created_at),
        'updated_at': str(user.updated_at)
    })
