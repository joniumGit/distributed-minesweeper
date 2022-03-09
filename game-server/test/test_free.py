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


def test_initializing(client):
    cnt = 1000
    cnt2 = 500
    r = client.post('/start', params={'width': cnt, 'height': cnt2, 'mines': int(cnt * cnt2 * 0.6)})
    assert r.status_code == 201, r.content
    loc = r.headers['Location']
    r = client.get(loc)
    assert r.status_code == 202
    i = 0
    while i < 200:  # Timeout at 2 secs
        import time
        time.sleep(0.01)
        r = client.get(loc)
        if r.status_code != 200:
            i += 1
        else:
            break
    assert i >= 0


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
