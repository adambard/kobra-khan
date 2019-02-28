import time
import logging

from starlette.applications import Starlette
from starlette.responses import JSONResponse
import uvicorn

from libsnek.data import BoardState
from libsnek import minimax

from kobrakhan import snake

COLOR = "#4e10d3"
HEAD_TYPE = "tongue"
TAIL_TYPE = "round-bum"


logger = logging.getLogger(__name__)

logger.setLevel(logging.DEBUG)


app = Starlette()


def get_move(weights):
    u, r, d, l = weights

    if u >= r and u >= d and u >= l:
        return "up"
    elif r >= d and r >= l:
        return "right"
    elif d >= l:
        return "down"
    else:
        return "left"


async def calculate_move(board_state_raw):
    start = time.time()

    board_state = BoardState(board_state_raw)

    logger.info("=== Game: %s, Turn: %d, Snake: %s ===", board_state.id, board_state.turn, board_state.you.id)

    # Kick off heuristic calc
    heuristics = snake.apply(board_state)

    minimax_scores = minimax.apply(board_state, depth=3)
    logger.info("MINIMAX SCORES: %r", minimax_scores)

    minimax_done = time.time()

    heuristic_weights = await heuristics
    logger.info("HEURISTIC WEIGHTS: %r", heuristic_weights)

    heuristics_done = time.time()

    combined_weights = minimax_scores * heuristic_weights
    logger.info("COMBINED WEIGHTS: %r", combined_weights)

    move = get_move(combined_weights)

    end = time.time()

    logger.info("Minimax: %0.2fs", minimax_done - start)
    logger.info("Heuristics: %0.2fs", heuristics_done - minimax_done)
    logger.info("Elapsed time: %0.2fs", end - start)

    return move


@app.route('/start', methods=['POST'])
async def start(request):
    return JSONResponse({
        'color': COLOR,
        'headType': HEAD_TYPE,
        'tailType': TAIL_TYPE,
    })


@app.route('/move', methods=['POST'])
async def move(request):

    board_state_raw = await request.json()
    move = await calculate_move(board_state_raw)

    return JSONResponse({'move': move})


@app.route('/end', methods=['POST'])
async def end(request):
    return JSONResponse({})


@app.route('/ping', methods=['POST'])
async def ping(request):
    return JSONResponse({})


@app.route('/set_weights', methods=['POST'])
async def set_weights(request):
    body = await request.json()
    if "weights" in body:
        snake.set_weights(body['weights'])

    return JSONResponse({})


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
