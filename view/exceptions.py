from sanic.exceptions import InvalidUsage, Unauthorized, Forbidden, NotFound


class InvalidUsage(InvalidUsage):
    pass


class Unauthorized(Unauthorized):
    pass


class Forbidden(Forbidden):
    pass


class NotFound(NotFound):
    pass