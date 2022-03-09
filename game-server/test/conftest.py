import pytest
from fastapi.testclient import TestClient

from server.app import State, game_state, app

state_proxy = [State()]


class ProxyLog:

    @staticmethod
    def isEnabledFor(*_, **__):
        return True

    @staticmethod
    def info(_str):
        print(_str)


def proxy_state():
    print('Called State Proxy')
    return state_proxy[0]


app.dependency_overrides[game_state] = proxy_state


@pytest.fixture(scope='session')
def token_name():
    yield 'DS_BROKER_TOKEN'


@pytest.fixture(scope='session', autouse=True)
def token(token_name):
    from secrets import token_urlsafe
    from os import environ
    t = token_urlsafe(32)
    environ[token_name] = t
    yield t


@pytest.fixture(scope='function', autouse=True)
def state():
    print('State Invoked')
    State._LOG = ProxyLog
    state_proxy[0] = State()
    yield state_proxy[0]


@pytest.fixture(scope='function')
def client(token):
    from headers import AUTHORIZATION
    print('Client Invoked')
    with TestClient(app) as client:
        client.headers[AUTHORIZATION] = f"Bearer {token}"
        yield client
