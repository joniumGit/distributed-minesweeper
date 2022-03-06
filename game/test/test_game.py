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


def _setup(_field, funcs) -> Setup:
    w = len(_field[0])
    h = len(_field)
    data = funcs.list_to_array(_field)
    game = Minesweeper(w, h, sum(1 if i == 9 else 0 for fp in _field for i in fp))
    game._field._data = data
    field = game._field
    return Setup(game=game, field=field)


@pytest.fixture
def setup(funcs):
    yield _setup(FIELD, funcs)


@pytest.fixture
def setup2(funcs):
    yield _setup(FIELD2, funcs)


def test_no_move_on_flag(setup: Setup):
    game = setup.game
    field = setup.field
    sq = game.flag(1, 1).items[0]
    assert sq.flag and sq.x == 1 and sq.y == 1
    for x, y in iter_2d(4, 4):
        assert field[x, y] & OPEN == 0
    assert len(game.open(1, 1).items) == 0


def test_flood_removes_flag(setup: Setup):
    game = setup.game
    field = setup.field
    m = game.flag(1, 1)
    assert m.items[0].flag
    m = game.open(0, 0)
    assert any(map(lambda s: s.x == 1 and s.y == 1 and s.open, m.items))
    assert all(map(lambda s: s.open, m.items))
    assert field[1, 1] & FLAG == 0


def test_empty_no_action(setup: Setup):
    game = setup.game
    game.open(0, 0)
    assert len(game.open(0, 0).items) == 0
    assert game.open(0, 0).status is None


def test_no_flag_empty(setup: Setup):
    game = setup.game
    game.open(0, 0)
    assert len(game.flag(0, 0).items) == 0


def test_no_flood_on_number(setup2: Setup):
    game = setup2.game
    m = game.open(2, 0)
    assert len(m.items) == 1
    assert m.items[0].value == 1


def test_flood_8_and_win(setup2: Setup, funcs):
    from minesweeper.logic import OPEN, MINE
    from pprint import pformat
    game = setup2.game
    m = game.open(2, 2)
    assert all(list(map(lambda b: b & (OPEN | MINE), setup2.field._data)))
    assert setup2.field, '\n' + pformat(funcs.array_to_list(
        setup2.field._data,
        setup2.field.width,
        setup2.field.height
    ))
    assert m.status == 'win', '\n' + pformat(funcs.array_to_list(
        setup2.field._data,
        setup2.field.width,
        setup2.field.height
    ))
    assert len(m.items) == 17


def test_mine(setup2: Setup):
    game = setup2.game
    m = game.open(3, 0)
    assert m.status == 'lose'
    assert len(m.items) == 3  # All mines
    assert m.items[0].mine
    assert m.items[0].open


def test_initialize():
    g = Minesweeper(4, 4, 1)
    g.initialize()
    assert any(map(lambda i: i > 8, g._field._data))


def test_oob_throws():
    m = Minesweeper(8, 8, 10)
    m._field.generate()
    with pytest.raises(IndexError):
        m.open(10, 10)
    with pytest.raises(IndexError):
        m.flag(10, 10)


def test_properties():
    m = Minesweeper(5, 6, 7)
    assert m.width == 5
    assert m.height == 6
    assert m.mines == 7


def test_iterate(setup: Setup):
    setup.game.open(0, 0)
    should_be_open = [
        (0, 0),
        (1, 0),
        (2, 0),
        (3, 0),
        (0, 1),
        (1, 1),
        (2, 1),
        (3, 1),
        (2, 2),
        (3, 2),
    ]
    for s in setup.field:
        assert (s.x, s.y) in should_be_open


def test_iterate_2(setup: Setup):
    setup.game.open(1, 1)
    should_be_open = [
        (1, 1)
    ]
    for s in setup.field:
        assert (s.x, s.y) in should_be_open


def test_iterate_3(setup: Setup):
    setup.game.flag(1, 3)
    expected = [
        (1, 3)
    ]
    for s in setup.game:
        assert (s.x, s.y) in expected
        assert s.flag
        assert not s.open
    assert not setup.field


def test_check(setup: Setup):
    s = setup.game.check(0, 1)
    assert not s.open
    assert s.value is None
    assert not s.flag
    assert s.x == 0
    assert s.y == 1


def test_reg_flood_return_order(setup: Setup):
    """
    At one point the game and field returned unopened squares with wrong values
    in the wrong order. This checks the order, value, and that they are open.
    """
    m = setup.game.open(0, 0)
    order = [
        (1, 1, 1), (0, 1, 1), (0, 0, 0), (2, 1, 1), (1, 0, 0), (2, 0, 0), (3, 0, 0), (2, 2, 2), (3, 2, 1), (3, 1, 0)
    ]
    for idx, expected, got in zip(range(0, len(order)), order, m.items):
        out = f"[{idx}] Expected: {expected}, Got: ({got.x}, {got.y}, {got.value})"
        assert got.open, out
        assert got.x == expected[0], out
        assert got.y == expected[1], out
        assert got.value == expected[2], out


def test_full_iter(setup2: Setup, funcs):
    """
    Show everything on win
    """
    game = setup2.game
    game.open(2, 2)
    assert len(list(game)) == game.width * game.height


def test_iter_on_mine(setup2: Setup, funcs):
    """
    Show only mines and opened squares + flags
    """
    game = setup2.game
    game.open(2, 0)
    game.flag(2, 1)
    game.open(3, 0)
    assert len(list(game)) == game.mines + 1 + 1
