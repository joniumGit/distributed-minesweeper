from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List, Generator

from .logic import Field, Square


class Status(Enum):
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
    _status: Status = Status.ONGOING

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
        squares = list(self._field.open(x, y))
        if self._field:
            self._status = Status.WIN
            return Move(status=self._status, items=squares)
        elif len(squares) == 1:
            square = squares[0]
            if square.mine:
                self._status = Status.LOSE
                return Move(status=self._status, items=squares)
            else:
                return Move(items=squares)
        else:
            return Move(items=squares)

    def flag(self, x: int, y: int) -> Move:
        return Move(items=list(self._field.flag(x, y)))

    def __iter__(self) -> Generator[Square, None, None]:
        yield from self._field

    def check(self, x: int, y: int) -> Square:
        return self._field.check(x, y)

    @property
    def status(self) -> Status:
        return self._status

    def initialize(self):
        self._field.generate()


__all__ = ['Square', 'Move', 'Minesweeper', 'Status']
