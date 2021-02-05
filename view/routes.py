from typing import List
from typing import Callable

from sanic import Sanic

from controller.user.user_auth import user_auth
from controller.user.user_add_2fa import user_add_2fa
from controller.user.user_delete_2fa import user_delete_2fa
from controller.user.user_logout import user_logout
from controller.user.user_create import user_create
from controller.user.user_edit import user_edit
from controller.user.user_info import user_info
from controller.user.user_update_avatar import user_update_avatar
from controller.user.user_get_avatar import user_get_avatar

from controller.msg.msg_create import msg_create
from controller.msg.msg_get import msg_get
from controller.msg.msg_edit import msg_edit
from controller.msg.msg_delete import msg_delete
from controller.msg.msg_read import msg_read
from controller.msg.msg_get_photo import msg_get_photo


class Route:
    def __init__(self, app: Sanic, handler: Callable, uri: str, methods: List):
        self.app = app
        self.handler = handler
        self.uri = uri
        self.methods = methods
        self.app.add_route(handler, uri, methods)


def register_routes(app: Sanic):
    # USER
    Route(app, user_create, '/user', ['POST'])
    Route(app, user_info, '/user/<user_id:int>', ['GET'])
    Route(app, user_edit, '/user/<user_id:int>', ['PATCH'])
    Route(app, user_auth, '/auth', ['POST'])
    Route(app, user_add_2fa, '/user/add_2fa', ['GET', 'POST'])
    Route(app, user_delete_2fa, '/user/delete_2fa', ['POST'])
    Route(app, user_logout, '/logout', ['POST'])
    Route(app, user_update_avatar, '/user/<user_id:int>/avatar', ['PATCH'])
    Route(app, user_get_avatar, '/user/<user_id:int>/avatar', ['GET'])
    # MESSAGE
    Route(app, msg_create, '/msg', ['POST'])
    Route(app, msg_get, '/msg', ['GET'])
    Route(app, msg_edit, '/msg/<message_id:int>', ['PATCH'])
    Route(app, msg_delete, '/msg/<message_id:int>', ['DELETE'])
    Route(app, msg_read, '/msg/<message_id:int>', ['GET'])
    Route(app, msg_get_photo, '/msg/<message_id:int>/photo', ['GET'])






