import pytest


@pytest.fixture
def anyio_backend():
    return 'asyncio'


def list_to_array(data):
    """
    Convert 2D list with origin at upper left into internal array repr

    VALUE = X * HEIGHT + Y
    """
    from minesweeper.logic import MINE
    new_data = list(range(0, len(data[0]) * len(data)))
    for x in range(0, len(data[0])):
        for y in range(0, len(data)):
            new_data[x * len(data) + y] = (data[y][x] if data[y][x] != 9 else MINE)
    return bytearray(new_data)


def array_to_list(data, width, height):
    from minesweeper.logic import OPEN, MINE, TAIL

    def to_str(i):
        if i & MINE:
            return '(x)' if i & OPEN else '[x]'
        if i & OPEN:
            return f'({i & TAIL})'
        else:
            return f'[{i & TAIL}]'

    new_data = list(list('' for _ in range(0, width)) for _ in range(0, height))
    for x in range(0, width):
        for y in range(0, height):
            new_data[y][x] = to_str(data[x * height + y])
    return new_data


@pytest.fixture
def funcs():
    class Funcs:

        @property
        def array_to_list(self):
            return array_to_list

        @property
        def list_to_array(self):
            return list_to_array

    yield Funcs()
