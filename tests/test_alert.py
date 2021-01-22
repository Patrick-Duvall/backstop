import pytest
import datetime
from flaskr.db import get_db
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)


@pytest.mark.parametrize('path', (
    '/alerts/create',
    '/alerts/1/update',
    '/alerts/1/delete',
))
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers['Location'] == 'http://localhost/auth/login'


@pytest.mark.parametrize('path', (
    '/alerts/2/update',
    '/alerts/2/delete',
))
def test_resource_exists_post(client, auth, path):
    auth.login()
    assert client.post(path).status_code == 404


def test_resource_exists_get(client, auth):
    auth.login()
    assert client.get('alerts/2/edit').status_code == 404


def test_index(client, auth):
    response = client.get('/alerts')
    assert response.status_code == 302
    assert b"<title>Redirecting" in response.data

    auth.login()
    response = client.get('/alerts')
    assert b'Log Out' in response.data
    assert b'My Alerts' in response.data
    assert b'New Alert' in response.data
    assert b'Send overdue alert to test@test.com' in response.data
    assert b'action="/alerts/1/edit"' in response.data
    assert b'action="/alerts/1/delete"' in response.data


def test_create(client, auth, app):
    auth.login()
    client.post('/alerts/create',
                data={'title': 'test',
                      'message': 'test',
                      'email': 'test@',
                      'alert-date': '2020-01-01 00:00:01'}
                )

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM alert').fetchone()[0]
        assert count == 2


def test_edit(client, auth):
    auth.login()
    assert client.get('alerts/1/edit').status_code == 200


def test_update(client, auth, app):
    auth.login()
    # time = datetime.datetime.now()
    # post_time = time.strftime
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
    assert response.headers['Location'] == 'http://localhost/alerts'

    with app.app_context():
        db = get_db()
        alert = db.execute('SELECT * FROM alert WHERE id = 1').fetchone()
        assert alert is None
