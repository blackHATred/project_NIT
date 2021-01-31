import bcrypt
from view.exceptions import InvalidUsage


def hash_pass(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def check_pass(password, hashed_password):
    if not bcrypt.checkpw(password.encode('utf-8'), hashed_password): raise InvalidUsage('Password is incorrect')
