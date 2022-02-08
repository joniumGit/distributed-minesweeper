from dataclasses import dataclass, field
from typing import Optional, List

from .logic import Field, Square


@dataclass
class Move:
    win: Optional[bool] = None
    mine: Optional[bool] = None
    changed: List[Square] = field(default_factory=list)


class Minesweeper:
    _field: Field

    def __init__(self, width: int, height: int, mines: int):
        self._field = Field(width, height, mines)

    def open(self, x: int, y: int) -> Move:
        squares = list(self._field.open(x, y))
        if self._field:
            return Move(win=True, changed=squares)
        elif len(squares) == 1:
            square = squares[0]
            if square.mine:
                return Move(mine=True, win=False, changed=squares)
            else:
                return Move(changed=squares)
        else:
            return Move(changed=squares)

    def flag(self, x: int, y: int) -> Move:
        return Move(changed=list(self._field.flag(x, y)))

    def __await__(self):
        yield from self._field.__await__()


__all__ = ['Square', 'Move', 'Minesweeper']
