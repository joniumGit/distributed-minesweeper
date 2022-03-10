import pytest


def test_start_too_many_mines(client):
    r = client.post('/start', params={'width': 8, 'height': 8, 'mines': 95})
    assert r.status_code == 422
    assert r.json()['detail'][0]['msg'].startswith('Too many mines'), r.json()


def test_start_too_small_field(client):
    r = client.post('/start', params={'width': 2, 'height': 4, 'mines': 95})
    assert r.status_code == 422
    assert r.json()['detail'][0]['msg'].startswith('Bad dimensions'), r.json()


def test_start(client):
    r = client.post('/start', params={'width': 8, 'height': 8, 'mines': 10})
    assert r.status_code == 201


def _initializing(client, path=None, method=None):
    from server.models import MAX_HEIGHT, MAX_WIDTH
    r = client.post('/start', params={
        'width': MAX_WIDTH - 1,
        'height': MAX_HEIGHT - 1,
        'mines': int(MAX_WIDTH * MAX_HEIGHT * 0.6)
    })
    assert r.status_code == 201, f'Failed, got: {r.status_code}\n{r.content}'

    if path is None:
        path = r.headers['Location']

    if method is None:
        method = 'get'

    r = getattr(client, method)(path)
    assert r.status_code == 202

    i = 0
    while i < 200:
        import time
        r = getattr(client, method)(path)
        if r.status_code != 202:
            break
        i += 1
        time.sleep(0.01)
    assert i != 200


def test_initializing(client):
    _initializing(client)


@pytest.mark.parametrize('p,method', [
    ('/reload', 'get'),
    ('/check?x=0&y=0', 'get'),
    ('/open?x=0&y=0', 'post'),
    ('/flag?x=0&y=0', 'post'),
    ('/flag?x=0&y=0', 'delete'),
    ('/', 'get'),
])
def test_initializing_endpoints(client, p, method):
    _initializing(client, path=p, method=method)


def test_status(client):
    test_start(client)
    r = client.get('/reload')
    assert r.json()['status'] == 'ongoing'


def test_set_delete_flag(client):
    r = client.post('/start', params={'width': 8, 'height': 8, 'mines': 10})
    assert r.status_code == 201
    r = client.post('/flag', params={'x': 0, 'y': 0})
    assert r.status_code == 201
    r = client.post('/flag', params={'x': 0, 'y': 0})
    assert r.status_code == 304
    r = client.delete('/flag', params={'x': 0, 'y': 0})
    assert r.status_code == 204
    r = client.delete('/flag', params={'x': 0, 'y': 0})
    assert r.status_code == 304


def test_not_started(client):
    r = client.get('/')
    assert r.status_code == 404
    m = {'x': 0, 'y': 0}
    r = client.post('/open', params=m)
    assert r.status_code == 404
    r = client.post('/flag', params=m)
    assert r.status_code == 404
    r = client.delete('/flag', params=m)
    assert r.status_code == 404
    r = client.get('/reload')
    assert r.status_code == 404
    r = client.get('/check', params=m)
    assert r.status_code == 404


def test_flagging(client):
    from headers import LOCATION
    r = client.post('/start', params={'width': 8, 'height': 8, 'mines': 10})
    assert r.status_code == 201
    r = client.post('/flag', params={'x': 0, 'y': 0})
    assert LOCATION in r.headers
    assert r.status_code == 201
    loc = r.headers[LOCATION]
    r = client.get(loc)
    assert r.status_code == 200, loc
    assert r.json()['flag']
    r = client.delete('/flag', params={'x': r.json()['x'], 'y': r.json()['y']})
    assert LOCATION in r.headers
    assert r.status_code == 204
    r = client.get(r.headers[LOCATION])
    assert r.status_code == 200
    assert 'flag' not in r.json()
