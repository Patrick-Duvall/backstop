import pytest
from flaskr.db import get_db
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)


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
