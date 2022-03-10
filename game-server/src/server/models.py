import os
from typing import List, Optional, Iterable

from minesweeper.game import Minesweeper, Status
from pydantic import BaseModel, conint, Field, root_validator, validator

MAX_WIDTH = int(os.getenv('DS_MAX_WIDTH', '256'))
MAX_HEIGHT = int(os.getenv('DS_MAX_HEIGHT', '256'))


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
    width: conint(gt=0, lt=MAX_WIDTH)
    height: conint(gt=0, lt=MAX_HEIGHT)
    mines: conint(gt=0) = Field(..., description='Maximum is calculated via (width - 1)(height - 1)')

    @validator("width")
    def validate_width(cls, value):
        assert value < MAX_WIDTH, "Field too wide"
        return value

    @validator("height")
    def validate_height(cls, value):
        assert value < MAX_HEIGHT, "Field too tall"
        return value

    @root_validator(pre=False, skip_on_failure=True)
    def validate_combination(cls, value):
        from minesweeper.logic import check_dims
        width = value.get('width')
        height = value.get('height')
        mines = value.get('mines')
        check_dims(width, height, mines)
        return value


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
            name='y',
            type_=conint(ge=0, lt=game.height),
            model_config=BaseConfig,
            class_validators=None
        )
        cls.__schema_cache__.clear()

    def to_url(self):
        return f'x={self.x}&y={self.y}'


__all__ = [
    'Square',
    'Squares',
    'Start',
    'Result',
    'Move'
]
