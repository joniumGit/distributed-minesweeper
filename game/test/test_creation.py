import pytest

import minesweeper.logic
from minesweeper.logic import Field


def test_create_field():
    f = Field(10, 10, 8)
    assert f.width == 10
    assert f.height == 10
    assert f.mines == 8

    assert f._task is None
    assert f._data is None


@pytest.mark.anyio
@pytest.mark.parametrize('width,height,mines', [
    (10, 10, 8),
    (10, 10, 90),
    (100, 100, 0.27),
])
async def test_generate_field(width, height, mines):
    f = Field(width, height, int(width * height * mines) if not isinstance(mines, int) else mines)
    await f
    assert f._data is not None
    assert f._task is None
    assert len(f._data) == f.width * f.height
    assert len(list(filter(lambda sq: sq & minesweeper.logic.MINE, f._data))) == f.mines
    assert all(map(lambda sq: sq & minesweeper.logic.OPEN == 0, f._data))


def test_gen_field_same_seed():
    import os
    seed = os.urandom(8)
    f = Field(10, 12, 8, seed)
    f2 = Field(10, 12, 8, seed)
    f.generate()
    f2.generate(_override_inverse_check=True, _override=False)
    assert f._data is not None
    assert f2._data is not None
    assert f._data == f2._data


def test_to_dict():
    f = Field(10, 10, 8)
    f2 = Field.from_dict(f.dict())
    assert f == f2


def test_read_without_seed():
    f = Field.from_dict(dict(width=10, height=10, mines=8))
    assert f._seed is not None


def test_not_equals_seed():
    assert Field.from_dict(
        dict(width=10, height=10, mines=8, seed='AAAA')
    ) != Field.from_dict(
        dict(width=10, height=10, mines=8, seed='BBBB')
    )


def test_not_equals_mines():
    assert Field.from_dict(
        dict(width=10, height=10, mines=8, seed='AAAA')
    ) != Field.from_dict(
        dict(width=10, height=10, mines=9, seed='AAAA')
    )


def test_not_equals_height():
    assert Field.from_dict(
        dict(width=10, height=10, mines=8, seed='AAAA')
    ) != Field.from_dict(
        dict(width=10, height=9, mines=8, seed='AAAA')
    )


def test_not_equals_width():
    assert Field.from_dict(
        dict(width=10, height=10, mines=8, seed='AAAA')
    ) != Field.from_dict(
        dict(width=9, height=10, mines=8, seed='AAAA')
    )


def test_not_equals_type():
    assert Field.from_dict(
        dict(width=10, height=10, mines=8, seed='AAAA')
    ) != object()


def test_all_opened():
    from minesweeper.logic import iter_2d
    from itertools import starmap, chain
    f = Field(10, 10, 8)
    f.generate()
    assert not f
    for _ in chain.from_iterable(starmap(f.open, iter_2d(10, 10))):
        pass
    assert f


def test_flagged():
    f = Field(2, 2, 1)
    f.generate()
    assert next(f.flag(1, 1)).flag
    assert len(list(f.open(1, 1))) == 0
    assert not next(f.flag(1, 1)).flag
    assert len(list(f.open(1, 1))) == 1


def test_return_mine():
    from minesweeper.logic import MINE
    f = Field(4, 4, 1)
    f._data = bytearray([0, 0 | MINE, 0, 0])
    assert next(f.open(0, 1)).mine


@pytest.mark.parametrize('x,y', [
    (5, 6),
    (7, 6),
    (-1, None),
    (None, -2),
    (None, None),

])
def test_set_oob(x, y):
    f = Field(4, 4, 1)
    f.generate()
    with pytest.raises(IndexError) as e:
        next(f.open(x, y))
    assert str(e.value)[str(e.value).rfind('('):] == f'({x},{y})'
    with pytest.raises(IndexError) as e:
        f[x, y] = 0
    assert str(e.value)[str(e.value).rfind('('):] == f'({x},{y})'
