import os

from fastapi import FastAPI, Depends, APIRouter
from fastapi.responses import Response, JSONResponse, StreamingResponse
from headers import LOCATION
from pydantic import ValidationError

from .auth import AuthScheme
from .models import Start, Square, Result, Move
from .samples import OPEN_SAMPLES, RELOAD_SAMPLES, location, CHECK_SAMPLES
from .state import State

TESTING = os.getenv("DS_TESTING", "False").lower() == "true"
API_TAG = "API"
app = FastAPI(
    default_response_class=Response,
    openapi_tags=[
        {
            "name": API_TAG,
            "description": "Available API operations"
        }
    ],
    redoc_url=None,
    docs_url="/docs" if TESTING else None,
)
game_state = State()
auth = AuthScheme()
api = APIRouter(tags=[API_TAG], dependencies=[Depends(auth)])


@api.get(
    "/",
    status_code=200,
    responses={
        200: {
            "description": "Game has successfully been initialized."
        },
        202: {
            "description": "Game server is performing initial setup and is ready later."
        },
        404: {
            "description": "The game has not yet started."
        },
        410: {
            "description": "The game has ended."
        }
    }
)
def status(state: State = Depends(game_state)):
    state.status()


@api.post(
    "/start",
    name="start",
    status_code=201,
    responses={
        410: {
            "description": "The game has already started and this endpoint is gone."
        },
        422: {
            "description": "Some of the field parameters were invalid"
        },
        201: {
            "description": "The game started successfully."
        }
    }
)
def start_game(start: Start = Depends(), state: State = Depends(game_state)):
    state.initialize(start)
    return Response(status_code=201, headers=dict(location=app.url_path_for('status')))


@api.post(
    "/open",
    name="move",
    response_class=JSONResponse,
    status_code=200,
    response_model=Result,
    response_model_exclude_none=True,
    responses={
        200: {
            "description": "The square was successfully opened",
            "content": OPEN_SAMPLES
        },
        304: {
            "description": "The square was already open"
        },
        422: {
            "description": "Invalid model"
        },
        404: {
            "description": "The game has not yet started."
        },
    }
)
def make_move(move: Move = Depends(), state: State = Depends(game_state)):
    m = state.open(move.x, move.y)
    return Response(status_code=304) if m is None else m


@api.post(
    "/flag",
    status_code=201,
    responses={
        201: {
            "description": "Flag was created",
            "headers": location("Check url for the newly created flag `/check?x=0&y=0`")
        },
        304: {
            "description": "No change"
        },
        422: {
            "description": "Invalid model"
        },
        404: {
            "description": "The game has not yet started."
        },
    }
)
def add_flag(move: Move = Depends(), state: State = Depends(game_state)):
    return Response(status_code=state.flag(move.x, move.y, True), headers={
        LOCATION: f'{app.url_path_for("check")}?{move.to_url()}'
    })


@api.delete(
    "/flag",
    status_code=204,
    responses={
        204: {
            "description": "Flag was deleted",
            "headers": location("Check url for the affected square `/check?x=0&y=0`")
        },
        304: {
            "description": "No change"
        },
        422: {
            "description": "Invalid model"
        },
        404: {
            "description": "The game has not yet started."
        },
    }
)
def remove_flag(move: Move = Depends(), state: State = Depends(game_state)):
    return Response(status_code=state.flag(move.x, move.y, False), headers={
        LOCATION: f'{app.url_path_for("check")}?{move.to_url()}'
    })


@api.get(
    "/check",
    name="check",
    status_code=200,
    response_model=Square,
    response_class=JSONResponse,
    response_model_exclude_none=True,
    responses={
        200: {
            "description": "Successfully fetched square",
            "content": CHECK_SAMPLES
        },
        422: {
            "description": "Invalid parameters"
        },
        404: {
            "description": "The game has not yet started."
        },
    }
)
def check_square(move: Move = Depends(), state: State = Depends(game_state)):
    return state.check(move.x, move.y)


@api.get(
    "/reload",
    status_code=200,
    # response_model=Squares,
    response_class=StreamingResponse,
    responses={
        200: {
            "description": "Fetches the whole set of open squares on the field plus flags",
            "content": RELOAD_SAMPLES
        },
        404: {
            "description": "The game has not yet started."
        },
    }
)
async def reload(state: State = Depends(game_state)):
    return StreamingResponse(iter(state.all()), media_type="application/json")


async def handle_validation(_, exc: ValidationError):
    from fastapi.exception_handlers import request_validation_exception_handler
    from fastapi.exceptions import RequestValidationError
    from typing import cast

    return await request_validation_exception_handler(_, cast(RequestValidationError, exc))


app.add_exception_handler(ValidationError, handle_validation)
app.include_router(api)
