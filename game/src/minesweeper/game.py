from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List, Generator

from .logic import Field, Square


class IllegalStateError(RuntimeError):

    def __init__(self):
        super(IllegalStateError, self).__init__('Invalid game state')


class Status(Enum):
    INITIALIZING = 'initializing'
    ONGOING = 'ongoing'
    WIN = 'win'
    LOSE = 'lose'

    def __eq__(self, other):
        return self is other or self.value == other

    def __repr__(self):
        return self.value

    def __str__(self):
        return self.value


@dataclass
class Move:
    status: Optional[Status] = None
    items: List[Square] = field(default_factory=list)


class Minesweeper:
    _field: Field
    _status: Status = Status.INITIALIZING

    def __init__(self, width: int, height: int, mines: int):
        self._field = Field(width, height, mines)

    @property
    def width(self):
        return self._field.width

    @property
    def height(self):
        return self._field.height

    @property
    def mines(self):
        return self._field.mines

    def open(self, x: int, y: int) -> Move:
        if self.status is Status.ONGOING:
            squares = list(self._field.open(x, y))
            if self._field:
                self._status = Status.WIN
                squares.extend(self._field.iter_mines())
                return Move(status=self._status, items=squares)
            elif len(squares) == 1:
                square = squares[0]
                if square.mine:
                    self._status = Status.LOSE
                    squares.extend(self._field.iter_mines())
                    return Move(status=self._status, items=squares)
                else:
                    return Move(items=squares)
            else:
                return Move(items=squares)
        else:
            raise IllegalStateError()

    def flag(self, x: int, y: int) -> Move:
        if self.status is Status.ONGOING:
            return Move(items=list(self._field.flag(x, y)))
        else:
            raise IllegalStateError()

    def __iter__(self) -> Generator[Square, None, None]:
        if self.status is not Status.INITIALIZING:
            yield from self._field
            if self.status is not Status.ONGOING:
                yield from self._field.iter_mines()
        else:
            raise IllegalStateError()

    def check(self, x: int, y: int) -> Square:
        if self.status is not Status.INITIALIZING:
            return self._field.check(x, y)
        else:
            raise IllegalStateError()

    @property
    def status(self) -> Status:
        return self._status

    def initialize(self):
        if self.status is Status.INITIALIZING:
            self._field.generate()
            self._status = Status.ONGOING


__all__ = ['Square', 'Move', 'Minesweeper', 'Status']
