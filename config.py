import os


class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('ELEPHANT_SQL')
    SQLALCHEMY_TRACK_MODIFICATIONS=os.environ.get('SQLALCHEMY_TRACK')
    API_PUB_KEY = os.environ.get('API_PUBLIC_KEY')
    API_PRIV_KEY = os.environ.get('API_PRIVATE_KEY')