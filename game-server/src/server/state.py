import logging
import time
from threading import RLock
from typing import Optional

from fastapi import HTTPException, status

from minesweeper.game import Minesweeper, Status
from .models import Move, Square, Start


class State:
    _game: Optional[Minesweeper]
    initialized = False
    _LOG = logging.getLogger('uvicorn.access')

    _start: float = 0
    _stop_init: float = 0
    _stop_game: float = 0

    @property
    def log(self):
        return State._LOG

    def __init__(self):
        self._lock = RLock()
        self._game = None
        self._game_done = False

    def __call__(self):
        return self

    def _log_init_done(self):
        if self.log.isEnabledFor(logging.INFO):
            self.log.info(
                f'Game Initialization Finished, took: {round((self._stop_init - self._start) * 1000, 2):.2f} ms'
            )

    def _log_game_done(self):
        if self.log.isEnabledFor(logging.INFO):
            self.log.info(
                f'Game Finished, took: {round(self._stop_init - self._start, 2):.2f} s'
            )

    def _started(self):
        if self._game is None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Game Not Started')

    def _initialized(self):
        self._started()
        if not self.initialized:
            raise HTTPException(status_code=status.HTTP_202_ACCEPTED, detail='Initializing')

    def _done(self):
        self._initialized()
        if self._game_done:
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
            self.initialized = True
            self.__tread = None
        self._stop_init = time.time()
        self._log_init_done()

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
                    try:
                        self._start = time.time()
                        self._game = Minesweeper(start.width, start.height, start.mines)  # This can throw
                        Move.adapt(self._game)
                        self._start_init_task()
                        self.log.info('Initialized a game')
                        return  # Return here
                    except ValueError as e:
                        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.args[0])
        raise HTTPException(status_code=status.HTTP_410_GONE, detail='Already Started')

    def all(self):
        """
        Iterate all open and flagged squares
        """
        self._started()
        from dataclasses import asdict
        separator = ','.encode('utf-8')
        yield '{"items":['.encode('utf-8')
        for idx, square in enumerate(self._game):
            if idx != 0:
                yield separator
            yield Square.construct(Square.__fields_set__, **asdict(square)).json(exclude_none=True).encode('utf-8')
        yield f'],"status":"{self._game.status}"'.encode('utf-8')
        yield '}'.encode('utf-8')

    def flag(self, x: int, y: int, set_flag: bool) -> int:
        """
        Set or unset flag
        """
        with self._lock:
            s = self.game.check(x, y)
            if (set_flag and not s.flag) or (not set_flag and s.flag):
                m = self._game.flag(x, y)
                if len(m.items) != 0:
                    return 201
            return 304

    def check(self, x: int, y: int):
        """
        Check a square
        """
        self._started()
        return self._game.check(x, y)

    def open(self, x: int, y: int):
        """
        Make a move
        """
        with self._lock:
            m = self.game.open(x, y)
            if m.status is not None and m.status != Status.ONGOING:
                self._game_done = True
                self._stop_game = time.time()
                self._log_game_done()
            elif len(m.items) == 0:
                return None
            return m


__all__ = ['State']
