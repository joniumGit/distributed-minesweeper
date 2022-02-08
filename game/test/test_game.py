from dataclasses import dataclass

import pytest

from minesweeper import Minesweeper
from minesweeper.logic import iter_2d, OPEN, Field, FLAG

FIELD = [
    [0, 0, 0, 0],
    [1, 1, 1, 0],
    [1, 9, 2, 1],
    [1, 1, 2, 9]
]

FIELD2 = [
    [0, 0, 1, 9],
    [0, 0, 1, 1],
    [1, 1, 0, 0],
    [9, 2, 0, 0],
    [9, 2, 0, 0],
]


@dataclass
class Setup:
    game: Minesweeper
    field: Field


def _setup(_field) -> Setup:
    from conftest import list_to_array
    w = len(_field[0])
    h = len(_field)
    data = list_to_array(_field)
    game = Minesweeper(w, h, data.count(bytes([9])))
    game._field._data = data
    field = game._field
    return Setup(game=game, field=field)


@pytest.fixture
def setup():
    yield _setup(FIELD)


@pytest.fixture
def setup2():
    yield _setup(FIELD2)


def test_no_move_on_flag(setup: Setup):
    game = setup.game
    field = setup.field
    sq = game.flag(1, 1).changed[0]
    assert sq.flag and sq.x == 1 and sq.y == 1
    for x, y in iter_2d(4, 4):
        assert field[x, y] & OPEN == 0
    assert len(game.open(1, 1).changed) == 0


def test_flood_removes_flag(setup: Setup):
    game = setup.game
    field = setup.field
    m = game.flag(1, 1)
    assert m.changed[0].flag
    m = game.open(0, 0)
    assert any(map(lambda s: s.x == 1 and s.y == 1 and s.open, m.changed))
    assert field[1, 1] & FLAG == 0


def test_empty_no_action(setup: Setup):
    game = setup.game
    game.open(0, 0)
    assert len(game.open(0, 0).changed) == 0
    assert not game.open(0, 0).win
    assert not game.open(0, 0).mine


def test_no_flag_empty(setup: Setup):
    game = setup.game
    game.open(0, 0)
    assert len(game.flag(0, 0).changed) == 0


def test_no_flood_on_number(setup2: Setup):
    game = setup2.game
    m = game.open(2, 0)
    assert len(m.changed) == 1
    assert m.changed[0].value == 1


def test_flood_8_and_win(setup2: Setup):
    from minesweeper.logic import OPEN, MINE
    from conftest import array_to_list
    from pprint import pformat
    game = setup2.game
    m = game.open(2, 2)
    assert all(list(map(lambda b: b & (OPEN | MINE), setup2.field._data)))
    assert setup2.field, '\n' + pformat(array_to_list(setup2.field._data, setup2.field.width, setup2.field.height))
    assert m.win, '\n' + pformat(array_to_list(setup2.field._data, setup2.field.width, setup2.field.height))
    assert not m.mine
    assert len(m.changed) == 17


def test_mine(setup2: Setup):
    game = setup2.game
    m = game.open(3, 0)
    assert not m.win
    assert m.mine
    assert len(m.changed) == 1
    assert m.changed[0].mine
    assert m.changed[0].open


@pytest.mark.anyio
async def test_await():
    g = Minesweeper(100, 100, 1)
    await g
    if g._field._data[0] > 8:
        assert g.open(5, 5).win
    else:
        assert g.open(0, 0).win
