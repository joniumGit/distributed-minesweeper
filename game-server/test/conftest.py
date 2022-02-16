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


@pytest.fixture(scope='function', autouse=True)
def state():
    print('State Invoked')
    State._LOG = ProxyLog
    state_proxy[0] = State()
    yield state_proxy[0]


@pytest.fixture(scope='function')
def client():
    print('Client Invoked')
    with TestClient(app) as client:
        yield client
