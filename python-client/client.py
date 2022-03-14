import time
from typing import List, Optional, Tuple, Union

import headers
import requests

field: List[List[Optional[Union[int, str]]]] = [[]]


def get_node() -> Tuple[str, str]:
    r = requests.post('http://localhost/start')
    assert r.status_code == 201, r
    print('Got Node')
    time.sleep(2)
    print('Starting')
    return r.headers[headers.LOCATION], r.headers[headers.AUTHORIZATION]


def init_field(node_start: str) -> str:
    global field
    while True:
        try:
            width = int(input('Width: '))
            height = int(input('Height: '))
            mines = int(input('Mines: '))
            r = client.post(node_start, params=dict(width=width, height=height, mines=mines))
            assert r.status_code == 201, r
            field = [[None for _ in range(0, width)] for _ in range(0, height)]
            print('Field Done')
            return r.headers[headers.LOCATION]
        except (ValueError, AssertionError):
            print('Failed...')


def print_field():
    print('  ' + ' '.join(f'{i}' for i in range(0, len(field[0]))))
    for idx, row in enumerate(field):
        print(f'{idx}|' + ' '.join(' ' if v is None else f'{v}' for v in row))


def get_input() -> Tuple[bool, int, int]:
    while True:
        input_ = input('Give (f,)x,y: ')
        parts = input_.split(',')
        try:
            if len(parts) == 3:
                f, x, y = parts
                x = int(x)
                y = int(y)
                f = True
            else:
                x, y = parts
                x = int(x)
                y = int(y)
                f = False
            break
        except ValueError:
            print('Invalid Input')
    return f, x, y


def handle_flag(x: int, y: int):
    if field[y][x] == 'f':
        client.delete(f'{node}flag', params=dict(x=x, y=y))
        field[y][x] = None
    elif field[y][x] is None:
        client.post(f'{node}flag', params=dict(x=x, y=y))
        field[y][x] = 'f'


def handle_open(x: int, y: int) -> bool:
    r = client.post(f'{node}open', params=dict(x=x, y=y))
    if r.status_code == 200:
        for s in r.json()['items']:
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
            return True
    return False


LOCATION, AUTH = get_node()
with requests.Session() as client:
    client.headers[headers.AUTHORIZATION] = AUTH
    node = init_field(LOCATION)
    while True:
        print_field()
        f_, x_, y_ = get_input()
        if f_:
            handle_flag(x_, y_)
        elif handle_open(x_, y_):
            break
