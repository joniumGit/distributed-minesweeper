import pytest


@pytest.fixture(scope='function', autouse=True)
def initialized(state):
    print('Fixed Setup Invoked')
    from minesweeper.game import Minesweeper, Status
    from minesweeper.logic import Field, MINE, FLAG, TAIL, OPEN
    from server.models import Move

    field = Field(5, 6, 2)
    game = Minesweeper(5, 6, 2)
    game._field = field
    game._status = Status.ONGOING

    field._data = bytearray([0 for _ in range(0, 5 * 6)])

    # X 1 0 0 0
    # 2 2 1 0 F
    # 1 X 1 0 0
    # 1 1 F 0 0
    # 0 0 0 0 0
    # 0 0 0 0 0

    field[0, 0] |= MINE
    field[1, 1] += 1
    field[1, 0] += 1
    field[0, 1] += 1

    field[1, 2] |= MINE
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            else:
                field[1 + i, 2 + j] += 1

    field[2, 3] |= FLAG
    field[4, 1] |= FLAG

    for i in range(0, 6):
        for j in range(0, 5):
            v = field[j, i]
            print(v & TAIL if v & MINE == 0 else 'x', end='')
        print()
    state._game = game
    state.initialized = True
    Move.adapt(game)  # Very important

    yield

    for i in range(0, 6):
        for j in range(0, 5):
            v = field[j, i]
            print(f'{bool(v & OPEN):d}' if v & MINE == 0 else 'x', end='')
        print()


def test_field_setup(client, state):
    from minesweeper.logic import TAIL

    field = state.game._field
    game = state.game

    assert field[1, 1] & TAIL == 2
    assert game.check(2, 3).flag
    assert game.check(4, 1).flag

    r = client.get('/check', params={'x': 2, 'y': 3})
    assert r.status_code == 200, f'{r.status_code}-{r.text}'
    assert r.json()['flag'], f'{r.text}-{r.headers}'


def test_start_throws(client):
    r = client.post('/start', params=dict(width=8, height=8, mines=10))
    assert r.status_code == 410


def hit_mine(client):
    r = client.post('/open', params={'x': 0, 'y': 0})
    assert r.status_code == 200, r.content
    d = r.json()
    try:
        assert len(d['items']) == 2, d
        assert d['items'][0]['mine'], d
        assert d['items'][1]['mine'], d
        assert d['status'] == 'lose', d
    except KeyError as e:
        assert False, str(e) + '-' + str(d)


@pytest.mark.parametrize('path', [
    '/flag',
    '/open',
])
def test_mine_lose(client, path):
    hit_mine(client)
    r = client.post(path, params={'x': 0, 'y': 0})
    assert r.status_code == 410


def test_mine_check_ok(client):
    hit_mine(client)
    r = client.get('/check', params=dict(x=0, y=0))
    assert r.status_code == 200
    assert r.json()['mine']
    assert r.json()['open']


def test_mine_reload_ok(client):
    client.post('/open', params={'x': 0, 'y': 0})
    r = client.get('/reload')
    assert r.status_code == 200
    assert r.json()['status'] == 'lose'
    assert len(r.json()['items']) == 4  # 2 Flags and a mine
    o = r.json()['items'][0]
    assert o['mine']
    assert o['open']
    o = r.json()['items'][1]
    assert o['flag']
    o = r.json()['items'][2]
    assert o['flag']


def test_open_twice(client):
    r = client.post('/open', params={'x': 1, 'y': 0})
    assert r.status_code == 200
    r = client.post('/open', params={'x': 1, 'y': 0})
    assert r.status_code == 304


def test_gone(client):
    hit_mine(client)
    r = client.get('/')
    assert r.status_code == 410
    r = client.post('/flag', params={'x': 0, 'y': 0})
    assert r.status_code == 410
    r = client.delete('/flag', params={'x': 0, 'y': 0})
    assert r.status_code == 410
    r = client.post('/open', params={'x': 0, 'y': 0})
    assert r.status_code == 410
    r = client.post('/start', params={'width': 10, 'height': 10, 'mines': 16})
    assert r.status_code == 410
    r = client.get('/check', params={'x': 0, 'y': 0})
    assert r.status_code == 200
    r = client.get('/reload')
    assert r.status_code == 200


def test_win(client, state):
    # X 1 0 0 0
    # 2 2 1 0 F
    # 1 X 1 0 0
    # 1 1 F 0 0
    # 0 0 0 0 0
    # 0 0 0 0 0
    client.post('/open', params={'x': 4, 'y': 0})
    client.post('/open', params={'x': 0, 'y': 1})
    r = client.post('/open', params={'x': 0, 'y': 2})
    assert r.status_code == 200
    assert r.json()['status'] == 'win'
    assert len(r.json()['items']) == 3
    assert len(client.get('/reload').json()['items']) == 30


def test_location(client):
    """If model adaption is wrong this might fail
    """
    from headers import LOCATION
    client.post('/open?x=3&y=0')

    r = client.post('/open?x=3&y=0')
    assert r.status_code == 304
    assert r.headers[LOCATION].endswith('x=3&y=0')

    r = client.post('/open?x=0&y=3')
    assert r.status_code == 304
    assert r.headers[LOCATION].endswith('x=0&y=3')
