from starlette.applications import Starlette
from starlette.responses import JSONResponse
import uvicorn

import logging

from pprint import pprint
from pandas import *

from data import BoardState
from heuristics import nokillsnek


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


app = Starlette()

def get_weights(board_state):
    # TODO more smartness
    return nokillsnek.apply(board_state)


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
    board_state_raw = await request.json()
    # pprint(board_state_raw)

    board_state = BoardState(board_state_raw)
    print(DataFrame(board_state.state))

    weights = get_weights(board_state)

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
