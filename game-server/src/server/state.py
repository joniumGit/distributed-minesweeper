import logging
import time
from threading import RLock
from typing import Optional

from fastapi import HTTPException, status
from minesweeper.game import Minesweeper, Status

from .models import Move, Square, Start


def _iter_game(game: Minesweeper):
    from dataclasses import asdict
    separator = ','.encode('utf-8')
    yield '{"items":['.encode('utf-8')
    for idx, square in enumerate(game):
        if idx != 0:
            yield separator
        yield Square.construct(Square.__fields_set__, **asdict(square)).json(exclude_none=True).encode('utf-8')
    yield f'],"status":"{game.status}"'.encode('utf-8')
    yield '}'.encode('utf-8')


class State:
    _log: logging.Logger = logging.getLogger('uvicorn.error')
    _lock: RLock
    _game: Optional[Minesweeper]
    _start: float = 0
    _stop_init: float = 0
    _stop_game: float = 0

    @property
    def log(self):
        return State._log

    def __init__(self):
        self._lock = RLock()
        self._game = None

    def __call__(self):  # pragma: nocover
        """For FastAPI compatibility
        """
        return self

    def _started(self):
        if self._game is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Game Not Started')

    def _initialized(self):
        self._started()
        if self._game.status is Status.INITIALIZING:
            raise HTTPException(status_code=status.HTTP_202_ACCEPTED, detail='Initializing')

    def _done(self):
        self._initialized()
        if self._game.status is not Status.ONGOING:
            raise HTTPException(status_code=status.HTTP_410_GONE, detail='Game Ended')

    def status(self):
        """
        Check status
        """
        self._done()

    @property
    def game(self):
        """
        Check common conditions ang get game
        """
        self._done()
        return self._game

    def _initialize(self):
        """
        Wait for field init
        """
        self._game.initialize()
        with self._lock:
            self.__tread = None
        self._stop_init = time.time()
        self.log.info(
            f'Game Initialization Finished, took: {round((self._stop_init - self._start) * 1000, 2):.2f} ms'
        )

    def _start_init_task(self):
        import threading
        self.__tread = threading.Thread(target=self._initialize, daemon=True)
        self.__tread.start()

    def initialize(self, start: Start):
        """
        Initialize a game
        """
        if self._game is None:
            with self._lock:
                if self._game is None:
                    self._start = time.time()
                    self._game = Minesweeper(start.width, start.height, start.mines)  # Validated so won't throw
                    Move.adapt(self._game)
                    self._start_init_task()
                    self.log.info('Initialized a game')
                    return  # Return here
        raise HTTPException(status_code=status.HTTP_410_GONE, detail='Already Started')

    def all(self):
        """
        Iterate all open and flagged squares
        """
        self._initialized()
        return _iter_game(self._game)

    def flag(self, x: int, y: int, set_flag: bool) -> int:
        """
        Set or unset flag
        """
        with self._lock:
            s = self.game.check(x, y)
            if (set_flag and not s.flag) or (not set_flag and s.flag):
                m = self._game.flag(x, y)
                if len(m.items) != 0:
                    return 201 if set_flag else 204
            return 304

    def check(self, x: int, y: int):
        """
        Check a square
        """
        self._initialized()
        return self._game.check(x, y)

    def open(self, x: int, y: int):
        """
        Make a move
        """
        with self._lock:
            m = self.game.open(x, y)
            if m.status is not None and m.status is not Status.ONGOING:
                self._stop_game = time.time()
                self.log.info(
                    f'Game Finished, took: {round(self._stop_game - self._start, 2):.2f} s'
                )
            elif len(m.items) == 0:
                return None
            return m


__all__ = ['State']
