import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY', 'hard to guess string')
    SSL_DISABLE = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True  # enable auto commit after request
    DASHBOARD_ADMIN = os.environ.get('DASHBOARD_ADMIN', 'admin@Supervisor.com')
    POSTS_PER_PAGE = 5
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = \
        os.environ.get(
            'DEV_DATABASE_URL',
            'postgresql://postgres:aisino123.@172.16.21.2:5432/db_dev'
        )
    COBBLER_SERVER_URL = \
        os.environ.get(
            'DEV_COBBLER_URL',
            'http://172.16.21.2:4321/cobbler_api'
        )
    COBBLER_USER = \
        os.environ.get(
            'DEV_COBBLER_USER',
            'cobbler'
        )
    COBBLER_PASSWORD = \
        os.environ.get(
            'DEV_COBBLER_PASSWORD',
            'aisino'
        )
