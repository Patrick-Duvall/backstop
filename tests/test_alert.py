import pytest
from urllib.parse import urlparse
import datetime
from app.db import get_db
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)

from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
#  with client.session_transaction() as session:
#      session['user_id'] = 'abc123' Stubs user login with google oauth

from app.user import User


@pytest.mark.parametrize('path', (
    '/alerts/create',
    '/alerts/1/update',
    '/alerts/1/delete',
))
def test_login_required(client, path):
    response = client.post(path, follow_redirects=True)
    assert b'Please log in to access this page' in response.data
    # TODO Add url assertion
    # assert request.path == '/'

@pytest.mark.parametrize('path', (
    '/alerts/2/update',
    '/alerts/2/delete',
))
def test_resource_exists_post(client, auth, path):
    session['user_id'] = 'abc123'
    assert client.post(path).status_code == 404


def test_resource_exists_get(client, auth):
    with client.session_transaction() as session:
        session['user_id'] = 'abc123'
    assert client.get('alerts/2/edit').status_code == 404


@pytest.mark.parametrize('path', (
    '/alerts/2/update',
    '/alerts/2/delete',
))
def test_resource_exists_post(client, auth, path):
    with client.session_transaction() as session:
        session['user_id'] = 'abc123'
    assert client.post(path).status_code == 404

def test_index(client, auth):
    response = client.get('/alerts', follow_redirects=True)
    assert response.status_code == 200
    assert b"<div class=\"flash\">Please log in to access this page.</div>" in response.data

    with client.session_transaction() as session:
        session['user_id'] = 'abc123'
    response = client.get('/alerts')
    assert b'Log Out' in response.data
    assert b'My Alerts' in response.data
    assert b'New Alert' in response.data
    assert b'Send overdue alert to test@test.com' in response.data
    assert b'action="/alerts/1/edit"' in response.data
    assert b'action="/alerts/1/delete"' in response.data


def test_create(client, auth, app):
    with app.test_request_context():
        with client.session_transaction() as session:
            session['user_id'] = 'abc123'
        response = client.post('/alerts/create',
            data={'title': 'test1',
                    'message': 'test1',
                    'email': 'test1@test.com',
                    'alert-date': '2020-01-01 00:00:01'},
            follow_redirects=True
            )
        assert response.status_code == 200
        assert b'<title>My Alerts - app' in response.data

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM alert').fetchone()[0]
        assert count == 2


def test_edit(client, auth, app):
    with app.test_request_context():
        with client.session_transaction() as session:
            session['user_id'] = 'abc123'
        assert client.get('alerts/1/edit').status_code == 200


def test_update(client, auth, app):
    with app.test_request_context():
        with client.session_transaction() as session:
            session['user_id'] = 'abc123'
        client.post('alerts/1/update', data={
            'title': 'updated',
            'message': 'updated',
            'email': 'updated',
            'schedule': '2020-01-01 00:00:02'
        })

    with app.app_context():
        db = get_db()
        alert = db.execute('SELECT * FROM alert WHERE id = 1').fetchone()
        assert alert['title'] == 'updated'
        assert alert['message'] == 'updated'
        assert alert['email'] == 'updated'
        assert alert['schedule'] == '2020-01-01 00:00:02'


def test_delete(client, auth, app):
    with app.test_request_context():
        with client.session_transaction() as session:
            session['user_id'] = 'abc123'
        response = client.post('alerts/1/delete', follow_redirects=True)
        assert response.status_code == 200
        assert b'<title>My Alerts - app' in response.data

    with app.app_context():
        db = get_db()
        alert = db.execute('SELECT * FROM alert WHERE id = 1').fetchone()
        assert alert is None
