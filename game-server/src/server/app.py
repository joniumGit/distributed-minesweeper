from fastapi import FastAPI, Depends, HTTPException, Body
from fastapi.responses import Response, JSONResponse, StreamingResponse
from headers import LOCATION

from .models import Start, Square, Result, Move
from .samples import OPEN_SAMPLES, RELOAD_SAMPLES, START_SAMPLES, location, CHECK_SAMPLES
from .state import State

API_TAG = "API"
app = FastAPI(default_response_class=Response, openapi_tags=[
    {
        "name": API_TAG,
        "description": "Available API operations"
    }
])
game_state = State()


@app.get(
    "/",
    tags=[API_TAG],
    status_code=200,
    responses={
        200: {
            "description": "Game has successfully been initialized."
        },
        202: {
            "description": "Game server is performing initial setup and is ready later."
        },
        403: {
            "description": "The game has not yet started."
        },
        410: {
            "description": "The game has ended."
        }
    }
)
def status(state: State = Depends(game_state)):
    try:
        state.status()
    except HTTPException as e:
        return Response(status_code=e.status_code)


@app.post(
    "/start",
    tags=[API_TAG],
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
def start_game(start: Start = Body(..., examples=START_SAMPLES), state: State = Depends(game_state)):
    state.initialize(start)
    return Response(status_code=201, headers=dict(location=app.url_path_for('status')))


@app.post(
    "/open",
    tags=[API_TAG],
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
        }
    }
)
def make_move(move: Move = Body(..., example=Move(x=0, y=0).json()), state: State = Depends(game_state)):
    m = state.open(move.x, move.y)
    return Response(status_code=304) if m is None else m


@app.post(
    "/flag",
    tags=[API_TAG],
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
        }
    }
)
def add_flag(move: Move, state: State = Depends(game_state)):
    return Response(status_code=state.flag(move.x, move.y, True), headers={
        LOCATION: f'{app.url_path_for("check")}?{move.to_url()}'
    })


@app.delete(
    "/flag",
    tags=[API_TAG],
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
        }
    }
)
def remove_flag(move: Move, state: State = Depends(game_state)):
    return Response(status_code=state.flag(move.x, move.y, False), headers={
        LOCATION: f'{app.url_path_for("check")}?{move.to_url()}'
    })


@app.get(
    "/check",
    tags=[API_TAG],
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
        }
    }
)
def check_square(move: Move = Depends(), state: State = Depends(game_state)):
    return state.check(move.x, move.y)


@app.get(
    "/reload",
    tags=[API_TAG],
    status_code=200,
    # response_model=Squares,
    response_class=StreamingResponse,
    responses={
        200: {
            "description": "Fetches the whole set of open squares on the field plus flags",
            "content": RELOAD_SAMPLES
        }
    }
)
async def reload(state: State = Depends(game_state)):
    return StreamingResponse(iter(state.all()), media_type="application/json")
