import minesweeper
import pytest


def test_iter_2d_basic():
    assert list(minesweeper.logic.iter_2d(4, 2)) == [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1), (3, 0), (3, 1)]


@pytest.mark.parametrize('w, h', [(10, 10), (1, -2), (1, 2), (2, 1), (1, 1), (0, 0), (-1, -1), (2, 0), (0, 2)])
def test_iter_2d(w, h):
    test = []
    for i in range(0, w):
        for j in range(0, h):
            test.append((i, j))
    assert list(minesweeper.logic.iter_2d(w, h)) == test


def test_n8():
    # -1,-1        1,-1
    #        0, 0
    # -1, 1        1, 1
    from minesweeper.logic import n8, n8_safer, check_n8_safe
    assert list(n8(0, 0)) == [(1, -1), (1, 1), (-1, 1), (-1, -1), (1, 0), (0, 1), (-1, 0), (0, -1)]
    assert not check_n8_safe(0, 0, 2, 2)
    assert list(n8_safer(0, 0, 2, 2)) == [(1, 1), (1, 0), (0, 1)]
    assert list(n8_safer(1, 1, 3, 3)) == [(2, 0), (2, 2), (0, 2), (0, 0), (2, 1), (1, 2), (0, 1), (1, 0)]
    assert list(n8_safer(1, 1, 2, 2)) == [(0, 0), (0, 1), (1, 0)]
