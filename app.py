import time
import logging

from starlette.applications import Starlette
from starlette.responses import JSONResponse
import uvicorn

from libsnek.data import BoardState
from libsnek.util import timeit

from heuristics import genetic


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


@app.route('/start', methods=['POST'])
async def start(request):
    return JSONResponse({'color': 'purple'})


@app.route('/move', methods=['POST'])
async def move(request):
    start = time.time()
    board_state_raw = await request.json()

    board_state = BoardState(board_state_raw)
    weights = timeit(lambda: genetic.apply(board_state))

    logger.debug(weights)

    return JSONResponse({'move': get_move(weights)})


@app.route('/end', methods=['POST'])
async def end(request):
    return JSONResponse({})


@app.route('/ping', methods=['POST'])
async def ping(request):
    return JSONResponse({})



if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
