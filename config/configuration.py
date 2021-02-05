import os
import datetime


def upload_path(path: str):
    if os.path.exists(path):
        return path
    else:
        os.mkdir(path)
        return path


host = os.getenv('HOST', '0.0.0.0')
port = int(os.getenv('PORT', 8000))

DB_URL = os.getenv('DB_URL', 'sqlite:///db.sqlite3')

AUTH_TOKEN_LIFE_DURATION = datetime.timedelta(days=1)
# После клонирования репозитория SECRET_KEY должен быть сменён
SECRET_KEY = os.getenv('SECRET_KEY', b'\x94w\xd6\x12\xae\x9c48G\xb6e\xe6\xdf\x13\x16\xc0\x8f=6\x9c_\xed~M')

UPLOAD_DIR = upload_path(os.getcwd()+'\\uploads')
MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', 1048576))  # Указываетя в байтах

