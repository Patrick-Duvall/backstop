# import mock
from pytest_mock import mocker
import pytest
from flaskr.db import get_db
from flaskr import create_app
import datetime
from apscheduler.schedulers.background import BackgroundScheduler

def test_send_overdue_emails(app):
    with app.app_context():
        db=get_db()
        # uid = db.execute('SELECT id FROM user LIMIT 1;')
        # db.execute(
        #     'INSERT INTO alert (email, message, schedule, title, author_id)'
        #     ' VALUES (?, ?, ?, ?, ?)',
        #     ('test', 'message', '2020-01-01 00:00:02', 'title', g.user['id'])
        # )
        # db.commit()
        create_app().send_overdue_emails()
        alerts = db.execute('SELECT sent from ALERT')
        for alert in alerts: 
            assert alert == true


def test_set_alert_scheduler(app):
    with app.app_context():
        # with patch.object(BackgroundScheduler(), 'add_job') as mock:
        #     create_app()
        # mock.assert_called_with(send_overdue_emails, 'cron', second='30')
        spy = mocker.spy(create_app(), 'scheduler.addjob')
        create_app()
        spy.assert_called_once_with(21)

