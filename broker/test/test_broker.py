import pytest
from broker.app import app
from fastapi.testclient import TestClient
from headers import AUTHORIZATION, LOCATION


@pytest.fixture(scope='function')
def client():
    with TestClient(app) as cl:
        yield cl


def test_create(client):
    r = client.post('/start')
    assert r.status_code == 201
    assert r.headers[LOCATION] is not None
    assert r.headers[AUTHORIZATION] is not None


def test_passthrough(client):
    r = client.post('/start')
    assert r.status_code == 201

    r = client.post(
        f'{r.headers[LOCATION]}?width=4&height=4&mines=1',
        headers={AUTHORIZATION: r.headers[AUTHORIZATION]}
    )
    assert r.status_code == 201
