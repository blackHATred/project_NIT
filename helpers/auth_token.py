import jwt
import datetime

from config.configuration import AUTH_TOKEN_LIFE_DURATION, SECRET_KEY
from view.exceptions import Unauthorized, InvalidUsage


def encode_auth_token(user_id: int) -> str:
    """
    Генерация токена авторизации
    :param user_id: id пользователя
    :return: string токена
    """
    payload = {
        'exp': datetime.datetime.utcnow() + AUTH_TOKEN_LIFE_DURATION,
        'iat': datetime.datetime.utcnow(),
        'usid': user_id
    }
    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm='HS256'
    )


def decode_auth_token(token: str) -> int:
    """
    Декодирование токена авторизации
    :param token: str токен
    :return: id пользователя
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['usid']
    except jwt.ExpiredSignatureError:
        raise Unauthorized('Session expired. Please log in again')
    except jwt.InvalidTokenError:
        raise InvalidUsage('Invalid session token. Please log in again')
