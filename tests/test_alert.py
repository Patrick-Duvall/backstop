import pytest
from urllib.parse import urlparse
import datetime
from flaskr.db import get_db
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

from flaskr.user import User


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
    # auth.login()
    assert client.get('alerts/2/edit').status_code == 404


@pytest.mark.parametrize('path', (
    '/alerts/2/update',
    '/alerts/2/delete',
))
def test_resource_exists_post(client, auth, path):
    # auth.login()
    assert client.post(path).status_code == 404

def test_index(client, auth):
    response = client.get('/alerts')
    assert response.status_code == 401
    assert b"<title>401 Unauthorized</title>" in response.data

    auth.login()
    response = client.get('/alerts')
    assert b'Log Out' in response.data
    assert b'My Alerts' in response.data
    assert b'New Alert' in response.data
    assert b'Send overdue alert to test@test.com' in response.data
    assert b'action="/alerts/1/edit"' in response.data
    assert b'action="/alerts/1/delete"' in response.data


def test_create(client, auth, app):
    client.post('/alerts/create',
                data={'title': 'test',
                      'message': 'test',
                      'email': 'test@',
                      'schedule': '2020-01-01 00:00:01'}
                )

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM alert').fetchone()[0]
        assert count == 2


def test_edit(client, auth, app):
    with app.test_request_context():
        login_user(User.get('abc123'))
        assert client.get('alerts/1/edit').status_code == 200


def test_update(client, auth, app):
    auth.login()
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
    auth.login()
    response = client.post('alerts/1/delete')
    # import pdb; pdb.set_trace()
    # assert response.headers['Location'] == 'http://localhost/alerts'
    assert response.status_code == 302
    assert urlparse(response.location) == '/alerts'

    with app.app_context():
        db = get_db()
        alert = db.execute('SELECT * FROM alert WHERE id = 1').fetchone()
        assert alert is None
