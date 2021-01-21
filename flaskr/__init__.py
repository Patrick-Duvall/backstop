import os

from flask import Flask, render_template

from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)


def create_app(test_config=None):
    # create and configure the app
    application = Flask(__name__, instance_relative_config=True)
    login_manager = LoginManager()
    login_manager.init_app(application)
    application.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(application.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        application.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        application.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(application.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(application)

    from . import auth
    application.register_blueprint(auth.bp)

    from . import blog
    application.register_blueprint(blog.bp)
    application.add_url_rule('/', endpoint='index')

    from . import alerts
    application.register_blueprint(alerts.bp, url_prefix="/alerts")

    return application
