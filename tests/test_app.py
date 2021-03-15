
import pytest
from app.db import get_db
from app import create_app
from apscheduler.schedulers.background import BackgroundScheduler

# def test_send_overdue_emails(app):
# TODO Currently this function is an inner funciton defined in create_app due
# to the application factory pattern. The larger problem here is emails are being defined in
# create app. This problem likely has to be solved before adding any additional mail schedulers


def test_set_alert_scheduler(mocker):
    spy = mocker.spy(BackgroundScheduler, 'add_job')
    assert not spy.called
    create_app()
    assert spy.called
