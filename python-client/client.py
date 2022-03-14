import time

import headers
import requests

field = [[None for _ in range(0, 8)] for _ in range(0, 8)]

r = requests.post('http://localhost/start')
assert r.status_code == 201, r
node_start = r.headers[headers.LOCATION]
auth = r.headers[headers.AUTHORIZATION]
print('Got Node')

with requests.Session() as client:
    client.headers[headers.AUTHORIZATION] = auth
    time.sleep(2)
    print('Starting')
    r = client.post(node_start, params=dict(width=8, height=8, mines=10))
    assert r.status_code == 201, r
    node = r.headers[headers.LOCATION]
    print('Field Done')


    def print_field():
        print('  ' + ' '.join(f'{i}' for i in range(0, len(field))))
        for idx, row in enumerate(field):
            print(f'{idx}|' + ' '.join(' ' if v is None else f'{v}' for v in row))


    while True:
        print_field()
        x_y = input('Give (f)x,y: ')
        x, y = x_y.split(',')
        if 'f' in x:
            x = x[1]
            if field[int(y)][int(x)] == 'f':
                r = client.delete(f'{node}flag', params=dict(x=x, y=y))
                field[int(y)][int(x)] = None
            elif field[int(y)][int(x)] is None:
                r = client.post(f'{node}flag', params=dict(x=x, y=y))
                field[int(y)][int(x)] = 'f'
        else:
            r = client.post(f'{node}open', params=dict(x=x, y=y))
            if r.status_code == 200:
                for s in r.json()['items']:
                    value = None
                    if s.get('flag', False):
                        value = 'f'
                    elif s.get('mine', False):
                        if s.get('open', False):
                            value = 'x'
                        else:
                            value = '*'
                    else:
                        value = s.get('value', None)
                    field[s['y']][s['x']] = value
                if r.json().get('status', 'ongoing') != 'ongoing':
                    print_field()
                    print(r.json()['status'])
                    break
