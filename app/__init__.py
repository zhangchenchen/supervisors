from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
import logging
import logging.handlers
import os

# initialize flask extensions
# note, extensions are initalized with no Flask app instance because
# application factor is being used
bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.session_protection = 'strong'  # use strong session protection
login_manager.login_view = 'auth.login'  # set the endpoint for login page


def create_app():
    """
    Flask Application Factory that takes configuration settings and returns
    a Flask application.
    """
    # initalize instance of Flask application
    app = Flask(__name__)

    # import configuration settings into Flask application instance
    app.config.from_object(Config)

    # initialize Flask extensions
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)


    # initialize flask log  
    info_file_handler = logging.handlers.RotatingFileHandler("flask_log.txt", maxBytes=1048576, backupCount=20)
    info_file_handler.setLevel(logging.DEBUG)
    logging_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    info_file_handler.setFormatter(logging_format)
    app.logger.addHandler(info_file_handler)


    # redirect all http requests to https
    if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
        from flask.ext.sslify import SSLify
        sslify = SSLify(app)

    # register 'main' blueprint with Flask application
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # register 'auth' blueprint with Flask application
    from .auth import auth as auth_blueprint
    # the 'url_prefix' parameter means all routes defined in the blueprint will
    # be registered with the prefix '/auth' (e.g., '/auth/login')
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app
