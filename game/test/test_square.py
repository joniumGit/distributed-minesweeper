from minesweeper.logic import FLAG, OPEN, Square, MINE


def test_not_open():
    value = FLAG | 1
    s = Square.from_triple(0, 0, value)
    assert not s.open
    assert not s.value


def test_flag():
    value = OPEN | 1
    s = Square.from_triple(0, 0, value)
    assert s.open
    assert s.value == 1


def test_open_flag():
    value = OPEN | FLAG | 1
    s = Square.from_triple(0, 0, value)
    assert s.open
    assert s.value == 1


def test_open_mine():
    value = MINE | OPEN
    s = Square.from_triple(0, 0, value)
    assert s.open
    assert s.mine
    assert not s.value


def test_status():
    from minesweeper.game import Status
    assert Status.ONGOING == 'ongoing'
    assert Status.ONGOING is getattr(Status, 'ONGOING')
    assert Status.ONGOING == Status.ONGOING
