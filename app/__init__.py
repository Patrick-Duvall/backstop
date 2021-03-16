import logging
import os
from datetime import datetime
from flask import Flask
from flask_mail import Mail, Message
from apscheduler.schedulers.background import BackgroundScheduler
from flask_login import LoginManager
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

login_manager = LoginManager()
login_manager.login_view = '/'
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # configure the login manager
    db.init_app(app)
    migrate.init_app(app, db)
    from app import models

    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)

    # if test_config is None:  # load the instance config, if it exists, when not testing
    #     app.config.from_pyfile('config.py', silent=True)
    # else:  # load the test config if passed in
    #     app.config.from_mapping(test_config)

    # try:  # ensure the instance folder exists
    #     os.makedirs(app.instance_path)
    # except OSError:
    #     pass

    from . import auth
    app.register_blueprint(auth.bp)

    app.add_url_rule('/', endpoint='index')

    from . import alerts
    app.register_blueprint(alerts.bp, url_prefix="/alerts")

    logging.basicConfig()
    # logging.getLogger('apscheduler').setLevel(logging.DEBUG)

    mail = Mail(app)
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'backstopapp@gmail.com'
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    mail = Mail(app)

    def send_overdue_emails():
        with app.app_context():
            now = datetime.now()
            alerts = db.execute(
                'SELECT id, title, schedule, email, message, sent'
                ' FROM alert'
                f" WHERE schedule < '{now}' AND sent = false"
            ).fetchall()

            for alert in alerts:
                msg = Message(alert['title'], sender='backStopApp@gmail.com',
                            recipients=[alert['email']])
                msg.body = alert['message']
                mail.send(msg)
                db.execute(
                    f"UPDATE alert set sent = true WHERE id = {alert['id']}"
                )
                db.commit()
                return "Sent"

    scheduler = BackgroundScheduler()
    scheduler.add_job(send_overdue_emails, 'cron', second='30')
    scheduler.start()

    return app
