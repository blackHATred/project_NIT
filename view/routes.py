from sanic import Sanic

from controller.user.user_auth import user_auth
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

routes = ({'handler': user_create, 'uri': '/user', 'methods': ['POST']},
          {'handler': user_info, 'uri': '/user/<user_id:int>', 'methods': ['GET']},
          {'handler': user_edit, 'uri': '/user/<user_id:int>', 'methods': ['PATCH']},
          {'handler': user_auth, 'uri': '/auth', 'methods': ['POST']},
          {'handler': user_logout, 'uri': '/logout', 'methods': ['POST']},
          {'handler': user_update_avatar, 'uri': '/user/<user_id:int>/avatar', 'methods': ['PATCH']},
          {'handler': user_get_avatar, 'uri': '/user/<user_id:int>/avatar', 'methods': ['GET']},

          {'handler': msg_create, 'uri': '/msg', 'methods': ['POST']},
          {'handler': msg_get, 'uri': '/msg', 'methods': ['GET']},
          {'handler': msg_edit, 'uri': '/msg/<message_id:int>', 'methods': ['PATCH']},
          {'handler': msg_delete, 'uri': '/msg/<message_id:int>', 'methods': ['DELETE']},
          {'handler': msg_read, 'uri': '/msg/<message_id:int>', 'methods': ['GET']},
          {'handler': msg_get_photo, 'uri': '/msg/<message_id:int>/photo', 'methods': ['GET']}
          )


def all_routes(app: Sanic):
    for i in routes:
        app.add_route(handler=i['handler'],
                      uri=i['uri'],
                      methods=i['methods'])
