#TODO move mailer to here, currently having issue 

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from flask_mail import Mail, Message
from datetime import datetime
from flask import current_app
import logging

logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

def create_alert_mailer(app):

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'backStopApp@gmail.com'
    app.config['MAIL_PASSWORD'] = 'afh8afh8'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    mail = Mail(app)


    def send_overdue_emails():
        with app.app_context():
            now = datetime.now()
            alerts = get_db().execute(
                'SELECT a.id, title, schedule, email, message'
                ' FROM alert'
                f" WHERE a.schedule < {now}"
            ).fetchall()

            for alert in alerts:
                msg = Message(alert['title'], sender='backStopApp@gmail.com',
                    recipients=[alert['email']])
                msg.body = alerts['message']
                mail.send(msg)
            return "Sent"


    scheduler = BackgroundScheduler()
    scheduler.add_job(send_overdue_emails, 'cron', minute='*/1')
    scheduler.start()

