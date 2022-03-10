import os

from fastapi import FastAPI, Depends, APIRouter, Request
from fastapi.responses import Response, JSONResponse, StreamingResponse
from headers import LOCATION
from pydantic import ValidationError

from . import samples
from .auth import AuthScheme
from .models import Start, Square, Result, Move
from .state import State

TESTING = os.getenv('DS_TESTING', 'False').lower() == 'true'
API_TAG = 'API'
app = FastAPI(
    default_response_class=Response,
    openapi_tags=[
        {
            'name': API_TAG,
            'description': 'Available API operations'
        }
    ],
    redoc_url=None,
    docs_url='/docs' if TESTING else None,
    description="Simple Minesweeper server",
    title="Distributed Minesweeper"
)
game_state = State()
auth = AuthScheme()
api = APIRouter(tags=[API_TAG], dependencies=[Depends(auth)])


@api.get(
    '/',
    name='status',
    status_code=200,
    responses=samples.ENTRY
)
def status(r: Request, state: State = Depends(game_state)):
    state.status()
    return JSONResponse(
        status_code=200,
        content={'detail': 'Game is Ready to Play'},
        headers={LOCATION: r.url_for('open')}
    )


@api.post(
    '/start',
    name='start',
    status_code=201,
    responses=samples.START
)
def start_game(r: Request, start: Start = Depends(), state: State = Depends(game_state)):
    state.initialize(start)
    return Response(status_code=201, headers=dict(location=r.url_for('status')))


@api.post(
    '/open',
    name='open',
    response_class=JSONResponse,
    status_code=200,
    response_model=Result,
    response_model_exclude_none=True,
    responses=samples.OPEN
)
def make_move(r: Request, move: Move = Depends(), state: State = Depends(game_state)):
    m = state.open(move.x, move.y)
    return Response(status_code=304, headers={
        LOCATION: f'{r.url_for("check")}?{move.to_url()}'
    }) if m is None else m


@api.post(
    '/flag',
    name='flag_add',
    status_code=201,
    responses=samples.FLAG_ADD
)
def add_flag(r: Request, move: Move = Depends(), state: State = Depends(game_state)):
    return Response(status_code=state.flag(move.x, move.y, True), headers={
        LOCATION: f'{r.url_for("check")}?{move.to_url()}'
    })


@api.delete(
    '/flag',
    name='flag_delete',
    status_code=204,
    responses=samples.FLAG_DELETE
)
def remove_flag(r: Request, move: Move = Depends(), state: State = Depends(game_state)):
    return Response(status_code=state.flag(move.x, move.y, False), headers={
        LOCATION: f'{r.url_for("check")}?{move.to_url()}'
    })


@api.get(
    '/check',
    name='check',
    status_code=200,
    response_model=Square,
    response_class=JSONResponse,
    response_model_exclude_none=True,
    responses=samples.CHECK
)
def check_square(move: Move = Depends(), state: State = Depends(game_state)):
    return state.check(move.x, move.y)


@api.get(
    '/reload',
    name='reload',
    status_code=200,
    response_class=StreamingResponse,
    responses=samples.RELOAD
)
async def reload(state: State = Depends(game_state)):
    return StreamingResponse(iter(state.all()), media_type='application/json')


async def handle_validation(_, exc: ValidationError):
    from fastapi.exception_handlers import request_validation_exception_handler
    from fastapi.exceptions import RequestValidationError
    from typing import cast

    return await request_validation_exception_handler(_, cast(RequestValidationError, exc))


app.add_exception_handler(ValidationError, handle_validation)
app.include_router(api)
