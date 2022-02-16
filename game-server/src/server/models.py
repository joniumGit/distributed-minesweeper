from typing import List, Optional, Iterable

from pydantic import BaseModel, conint, Field

from minesweeper.game import Minesweeper, Status


class Square(BaseModel):
    x: conint(ge=0)
    y: conint(ge=0)
    open: Optional[bool]
    flag: Optional[bool]
    mine: Optional[bool]
    value: Optional[conint(ge=0, lt=9)]


class Squares(BaseModel):
    status: Status
    items: Iterable[Square]


class Start(BaseModel):
    width: conint(gt=0)
    height: conint(gt=0)
    mines: conint(gt=0)


class Result(BaseModel):
    status: Optional[Status]
    mine: Optional[bool]
    items: List[Square] = Field(default_factory=list)

    class Config:
        arbitrary_types_allowed = True


class Move(BaseModel):
    x: conint(ge=0)
    y: conint(ge=0)

    @classmethod
    def adapt(cls, game: Minesweeper):
        """
        Modify model constraints to reflect current game
        """
        from pydantic import BaseConfig
        from pydantic.fields import ModelField
        cls.__fields__['x'] = ModelField(
            name='x',
            type_=conint(ge=0, lt=game.width),
            model_config=BaseConfig,
            class_validators=None
        )
        cls.__fields__['y'] = ModelField(
            name='x',
            type_=conint(ge=0, lt=game.height),
            model_config=BaseConfig,
            class_validators=None
        )
        cls.__schema_cache__.clear()


__all__ = [
    'Square',
    'Squares',
    'Start',
    'Result',
    'Move'
]
