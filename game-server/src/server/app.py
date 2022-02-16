from fastapi import FastAPI, Depends
from fastapi.responses import Response, JSONResponse, StreamingResponse

from .models import Start, Square, Result, Move
from .state import State

app = FastAPI(default_response_class=Response)
game_state = State()


@app.get("/", status_code=200)
def status(state: State = Depends(game_state)):
    state.status()


@app.post("/start", name="start", status_code=201)
def start_game(start: Start, state: State = Depends(game_state)):
    state.initialize(start)
    return Response(status_code=201, headers=dict(location=app.url_path_for('status')))


@app.post(
    "/open",
    name="move",
    response_class=JSONResponse,
    status_code=200,
    response_model=Result,
    response_model_exclude_none=True
)
def make_move(move: Move, state: State = Depends(game_state)):
    m = state.open(move.x, move.y)
    return Response(status_code=304) if m is None else m


@app.post("/flag")
def add_flag(move: Move, state: State = Depends(game_state)):
    return Response(status_code=state.flag(move.x, move.y, True))


@app.delete("/flag")
def remove_flag(move: Move, state: State = Depends(game_state)):
    return Response(status_code=state.flag(move.x, move.y, False))


@app.post(
    "/check",
    name="check",
    status_code=200,
    response_model=Square,
    response_class=JSONResponse,
    response_model_exclude_none=True
)
def check_square(move: Move, state: State = Depends(game_state)):
    return state.check(move.x, move.y)


@app.get(
    "/reload",
    status_code=200,
    # response_model=Squares,
    response_class=StreamingResponse
)
async def reload(state: State = Depends(game_state)):
    return StreamingResponse(iter(state.all()), media_type="application/json")
