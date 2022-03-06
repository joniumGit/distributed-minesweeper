from dataclasses import dataclass
from typing import NoReturn, Dict, Any, Optional, Union, Tuple, Generator

MINE = 0x20
FLAG = 0x40
OPEN = 0x80
TAIL = 0x0f


def check_dims(width: int, height: int, mines: int):
    """Checks allowed field dimensions
    """
    if width is None or height is None or width < 4 or height < 4:
        raise ValueError(f'Bad dimensions, min: 4,4 got: {width},{height}')
    if mines > (width - 1) * (height - 1):
        raise ValueError(f'Too many mines, max: {(width - 1) * (height - 1)} got: {mines}')
    elif mines < 1:
        raise ValueError(f'Too few mines')


def iter_edges(width: int, height: int):
    """
    Iterate through edges

    0 6 8 3
    1     4
    2 7 9 5
    """
    from itertools import repeat
    yield from zip(repeat(0), range(0, height))
    yield from zip(repeat(width - 1), range(0, height))
    for x in range(1, width - 1):
        yield x, 0
        yield x, height - 1


def check_n8_safe(x: int, y: int, width: int, height: int):
    """
    Checks if bound checking is needed
    """
    if 0 < x - 1 and x + 1 < width:
        if 0 < y - 1 and y + 1 < height:
            return True
    return False


def iter_2d(width: int, height: int):
    """
    Iterates through all the points on a 2D plane.

    Assumes indexing [(0, width - 1), (0, height - 1)].

    The plane is iterated height first:

      - [0, 0], [0, 1], [0, 2], [1, 0] ...

    :param width:  Width, first dimension
    :param height: Height, second dimension
    """
    from itertools import repeat, chain
    yield from chain.from_iterable(map(lambda i: zip(repeat(i), range(0, height)), range(0, width)))


def n8_safer(x: int, y: int, width: int, height: int):
    """
    Bounds checking n8

    4 8 1
    7 X 5
    3 6 2
    """
    xm = x - 1
    xp = x + 1
    ym = y - 1
    yp = y + 1

    hx = xp < width
    lx = 0 <= xm
    hy = yp < height
    ly = 0 <= ym

    if hx and ly:
        yield xp, ym
    if hx and hy:
        yield xp, yp
    if lx and hy:
        yield xm, yp
    if lx and ly:
        yield xm, ym

    if hx:
        yield xp, y
    if hy:
        yield x, yp
    if lx:
        yield xm, y
    if ly:
        yield x, ym


def n8(x: int, y: int):
    """
    4 8 1
    7 X 5
    3 6 2
    """
    xm = x - 1
    ym = y - 1
    yp = y + 1
    xp = x + 1

    yield xp, ym
    yield xp, yp
    yield xm, yp
    yield xm, ym

    yield xp, y
    yield x, yp
    yield xm, y
    yield x, ym


@dataclass
class Square:
    """
    Helper class for a square.
    """
    x: int
    y: int
    open: Optional[bool] = None
    flag: Optional[bool] = None
    mine: Optional[bool] = None
    value: Optional[int] = None

    @staticmethod
    def from_triple(x: int, y: int, value: int):
        if value & OPEN:
            if value & MINE:
                return Square(x=x, y=y, open=True, mine=True)
            else:
                return Square(x=x, y=y, open=True, value=value & TAIL)
        elif value & FLAG:
            return Square(x=x, y=y, flag=True)
        else:
            return Square(x=x, y=y)


class Field:
    """
    Description for field data:

    B - 0000 0000
    0 -      0000
    1 -      0001
    2 -      0010
    3 -      0011
    4 -      0100
    5 -      0101
    6 -      0110
    7 -      0111
    8 -      1000
    M - 0100
    F - 0010
    O - 1000
    -------------
    y x ->
    |
    v

    The event streams generated from open and flag should be consumed
    """

    __slots__ = ['width', 'height', 'mines', '_seed', '_task', '_data', 'shuffle']

    def __init__(self, width: int, height: int, mines: int, seed: bytes = None):
        check_dims(width, height, mines)
        self.width = width
        self.height = height
        self.mines = mines
        if seed is None:
            from os import urandom
            self._seed = urandom(32)
        else:
            self._seed = seed
        self._task = None
        self._data = None

    def flag(self, x: int, y: int) -> Generator[Square, None, None]:
        """
        Flag a tile on the field yielding a result if the field changed
        """
        value = self[x, y]
        if value & OPEN == 0:
            if value & FLAG:
                self[x, y] = value ^ FLAG
                yield Square(x=x, y=y, flag=False)
            else:
                self[x, y] = value | FLAG
                yield Square(x=x, y=y, flag=True)

    def open(self, x: int, y: int) -> Generator[Square, None, None]:
        """
        Open a square on the field yielding squares that changed as a result
        """
        from itertools import starmap
        value = self[x, y]
        if value & (FLAG | OPEN) == 0:
            yield from starmap(Square.from_triple, self._flood(x, y))

    def check(self, x: int, y: int) -> Square:
        """
        Check without opening
        """
        return Square.from_triple(x, y, self[x, y])

    def iter_mines(self):
        """
        Iterate over all mines that are not open
        """
        for x, y in iter_2d(self.width, self.height):
            v = self[x, y]
            if v & MINE and v & OPEN == 0:
                yield Square(x=x, y=y, mine=True)

    def __iter__(self) -> Generator[Square, None, None]:
        """
        Iterate over all open squares
        """
        for x, y in iter_2d(self.width, self.height):
            v = self[x, y]
            if v & (OPEN | FLAG):
                yield Square.from_triple(x, y, v)

    def __getitem__(self, point: Tuple[int, int]) -> int:
        """
        Get a value from the field
        """
        if point[0] is not None and point[1] is not None and 0 <= point[0] < self.width and 0 <= point[1] < self.height:
            return self._data[point[0] * self.height + point[1]]
        else:
            raise IndexError(f'Out of field ({point[0]},{point[1]})')

    def __setitem__(self, point: Tuple[int, int], value: int):
        """
        Set a square in the field
        """
        if point[0] is not None and point[1] is not None and 0 <= point[0] < self.width and 0 <= point[1] < self.height:
            self._data[point[0] * self.height + point[1]] = value
        else:
            raise IndexError(f'Out of field ({point[0]},{point[1]})')

    def __bool__(self):
        """
        Check if game is completed
        """
        mop = MINE | OPEN
        return all(map(lambda b: b & mop, self._data))

    def __eq__(self, other: 'Field'):
        if isinstance(other, type(self)):
            return self.width == other.width \
                   and self.height == other.height \
                   and self.mines == other.mines \
                   and self._seed == other._seed
        return False

    def dict(self) -> Dict[str, Union[str, int]]:
        """
        Save the field into a dict
        """
        from base64 import b64encode
        return dict(
            width=self.width,
            height=self.height,
            mines=self.mines,
            seed=b64encode(self._seed, altchars=b'-_')
        )

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> 'Field':
        """
        Generate field from a dict.

        Seed is in base64
        """
        if 'seed' in d:
            seed = d['seed']
            if seed is not None:
                from base64 import b64decode
                d['seed'] = b64decode(seed, validate=True, altchars=b'-_')
        return Field(**d)

    def generate(self, *, _override_inverse_check: bool = False, _override: bool = None) -> NoReturn:
        """
        Allocate space for the field and generate mines
        """
        from random import Random
        from itertools import repeat, chain

        width = self.width
        height = self.height
        size = width * height
        mines = self.mines
        normal = mines / size < 0.50
        if _override_inverse_check:
            normal = _override
        rand = Random(self._seed)

        data = bytearray(chain(repeat(MINE, mines), repeat(0, size - mines)))
        rand.shuffle(data)

        if normal:
            for x in range(1, width - 1):
                for y in range(1, height - 1):
                    if data[x * height + y] & MINE:
                        for dx, dy in n8(x, y):
                            if data[dx * height + dy] & MINE == 0:
                                data[dx * height + dy] += 1
            for x, y in iter_edges(width, height):
                if data[x * height + y] & MINE:
                    for dx, dy in n8_safer(x, y, width, height):
                        if data[dx * height + dy] & MINE == 0:
                            data[dx * height + dy] += 1
        else:
            for x in range(1, width - 1):
                for y in range(1, height - 1):
                    if not (data[x * height + y] & MINE):
                        for dx, dy in n8(x, y):
                            if data[dx * height + dy] & MINE:
                                data[x * height + y] += 1
            for x, y in iter_edges(width, height):
                if not (data[x * height + y] & MINE):
                    for dx, dy in n8_safer(x, y, width, height):
                        if data[dx * height + dy] & MINE:
                            data[x * height + y] += 1

        self._data = data

    def _flood(self, x: int, y: int):
        from collections import deque

        q = deque()
        width = self.width
        height = self.height
        data = self._data

        value = data[x * height + y]
        if value & (MINE | TAIL | OPEN | FLAG):
            value = value | OPEN
            data[x * height + y] = value
            yield x, y, value
        else:
            q.append((x, y))
            while q:
                x, y = q.popleft()
                value = data[x * height + y]

                if value & OPEN:  # Skip open
                    continue

                value = (value | OPEN) ^ FLAG  # Open and remove flag
                data[x * height + y] = value  # Commit

                for dx, dy in (
                        n8(x, y)
                        if check_n8_safe(x, y, width, height)
                        else n8_safer(x, y, width, height)
                ):
                    dv = data[dx * height + dy]
                    if dv & (MINE | OPEN) == 0:  # If not mine or open
                        if dv & TAIL:  # Wouldn't continue
                            dv = (dv | OPEN) ^ FLAG
                            data[dx * height + dy] = dv
                            yield dx, dy, dv
                        else:
                            q.appendleft((dx, dy))

                yield x, y, value


__all__ = ['Field', 'Square', 'check_dims']
