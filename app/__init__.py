# app/__init__.py
import pdb

# third-party imports
from app.extensions import csrf
from logging.handlers import RotatingFileHandler
from flask import abort, Flask, render_template
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# local imports
from config import app_config

# db variable initialization
db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    # Configure logging
    #handler = logging.FileHandler(app.config['LOGGING_LOCATION'])
    #handler.setLevel(app.config['LOGGING_LEVEL'])
    #formatter = logging.Formatter(app.config['LOGGING_FORMAT'])
    #handler.setFormatter(formatter)
    #app.logger.addHandler(handler)

    # Use the App Engine Requests adapter. This makes sure that Requests uses
    # URLFetch.
    if app.config['GAE']:
        from google.appengine.ext import ndb
        requests_toolbelt.adapters.appengine.monkeypatch()

    csrf.init_app(app)

    db.init_app(app)

    migrate = Migrate(app, db)

    Bootstrap(app)

    from app import models

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "auth.login"

    @app.route('/500')
    def error():
        abort(500)

    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/403.html', title='Forbidden'), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html', title='Page Not Found'), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('errors/500.html', title='Server Error'), 500

    return app

    if app.config['GAE']:
        class Settings(ndb.Model):
            name = ndb.StringProperty()
            value = ndb.StringProperty()

            @staticmethod
            def get(name):
                NOT_SET_VALUE = "NOT SET"
                retval = Settings.query(Settings.name == name).get()
                if not retval:
                    retval = Settings()
                    retval.name = name
                    retval.value = NOT_SET_VALUE
                    retval.put()
                if retval.value == NOT_SET_VALUE:
                    raise Exception(('Setting %s not found in the database. A placeholder record has been created.' +
                       ' Go to the Developers Console for your app in App Engine, look up the Settings record with ' +
                       'name=%s and enter its value in that records value field.') % (name, name))
                return retval.value
