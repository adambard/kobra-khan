import numpy as np

from libsnek.math import rms
from libsnek.util import timeit
from . import nokillsnek, hungry, claustrophobic
import pprint


HEURISTICS = (
    # name, function, weight
    ("nokill", nokillsnek, 10.0),
    ("hungry", hungry, 1.0),
    ("claustrophobic", claustrophobic, 2.0),
)


def apply(board_state):
    weight_array = [
        weight * timeit(lambda: np.array(heuristic.apply(board_state)), name)
        for name, heuristic, weight in HEURISTICS
    ]
    print("==== TURN", board_state.turn, "====")
    pprint.pprint(weight_array)

    return [
        rms(weights)
        for weights in zip(*weight_array)
    ]
