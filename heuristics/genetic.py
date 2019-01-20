import numpy as np

from libsnek.math import rms
from . import nokillsnek, hungry, claustrophobic, greedy
import pprint


HEURISTICS = (
    # name, function, weight
    ("nokill", nokillsnek, 10.0),
    ("hungry", hungry, 1.0),
    ("greedy", greedy, 0.5),
    ("claustrophobic", claustrophobic, 2.0),
)


async def apply(board_state):

    future_weights = [
        (weight, heuristic.apply(board_state))
        for _name, heuristic, weight in HEURISTICS
    ]

    weight_array = [
        weight * np.array(await future)
        for weight, future in future_weights
    ]
    pprint.pprint(weight_array)

    return [
        rms(weights)
        for weights in zip(*weight_array)
    ]
