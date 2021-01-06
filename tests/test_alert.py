import pytest
from flaskr.db import get_db


def test_index(client, auth):
    response = client.get('/alerts')
    assert response.status_code == 308

    auth.login()
    response = client.get('/')
    assert b'Log Out' in response.data
    assert b'My Alerts' in response.data
    assert b'New Alert' in response.data
    assert b'Send overdue alert to test@test.com' in response.data
    assert b'href="/alerts/1/update"' in response.data
