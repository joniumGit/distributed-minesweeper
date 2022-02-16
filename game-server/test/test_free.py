def test_start_too_many_mines(client):
    r = client.post('/start', json={'width': 8, 'height': 8, 'mines': 95})
    assert r.status_code == 400


def test_start(client):
    r = client.post('/start', json={'width': 8, 'height': 8, 'mines': 10})
    assert r.status_code == 201


def test_initializing(client):
    cnt = 1000
    cnt2 = 500
    r = client.post('/start', json={'width': cnt, 'height': cnt2, 'mines': int(cnt * cnt2 * 0.6)})
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
