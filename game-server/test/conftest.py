import pytest
from fastapi.testclient import TestClient

from server.app import State, game_state, app

state_proxy = [State()]


class ProxyLog:

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


@pytest.fixture(scope='session')
def token_width():
    yield 'DS_MAX_WIDTH'


@pytest.fixture(scope='session')
def token_height():
    yield 'DS_MAX_HEIGHT'


def _set_token(name, token):
    from os import environ
    environ[name] = token
    return token


@pytest.fixture(scope='session', autouse=True)
def token(token_name):
    from secrets import token_urlsafe
    t = token_urlsafe(32)
    yield _set_token(token_name, t)


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
        client.headers[AUTHORIZATION] = f'Bearer {token}'
        yield client


@pytest.fixture
def run_async():
    from asyncio import new_event_loop

    def run_inside(coro, *args):
        loop = new_event_loop()
        try:
            return loop.run_until_complete(coro(*args))
        finally:
            loop.close()

    yield run_inside
