import logging
from datetime import datetime
from flask import Flask
from flask_mail import Mail, Message
from apscheduler.schedulers.background import BackgroundScheduler
import os

from flask import Flask, render_template, url_for

from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

from flaskr.user import User


def create_app(test_config=None):
    application = Flask(__name__, instance_relative_config=True)

    # configure the login manager
    login_manager = LoginManager()
    login_manager.login_view = '/'
    login_manager.init_app(application)

    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)


    application.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(application.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:  # load the instance config, if it exists, when not testing
        application.config.from_pyfile('config.py', silent=True)
    else:  # load the test config if passed in
        application.config.from_mapping(test_config)

    try:  # ensure the instance folder exists
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

    logging.basicConfig()
    logging.getLogger('apscheduler').setLevel(logging.DEBUG)

    mail = Mail(application)
    application.config['MAIL_SERVER'] = 'smtp.gmail.com'
    application.config['MAIL_PORT'] = 465
    application.config['MAIL_USERNAME'] = 'backstopapp@gmail.com'
    application.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    application.config['MAIL_USE_TLS'] = False
    application.config['MAIL_USE_SSL'] = True
    mail = Mail(application)

    def send_overdue_emails():
        with application.app_context():
            now = datetime.now()
            database = db.get_db()
            alerts = database.execute(
                'SELECT id, title, schedule, email, message, sent'
                ' FROM alert'
                f" WHERE schedule < '{now}' AND sent = false"
            ).fetchall()

            for alert in alerts:
                msg = Message(alert['title'], sender='backStopApp@gmail.com',
                            recipients=[alert['email']])
                msg.body = alert['message']
                mail.send(msg)
                database = db.get_db()
                database.execute(
                    f"UPDATE alert set sent = true WHERE id = {alert['id']}"
                )
                database.commit()
                return "Sent"

    scheduler = BackgroundScheduler()
    scheduler.add_job(send_overdue_emails, 'cron', second='30')
    scheduler.start()

    return application



