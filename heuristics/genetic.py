import numpy as np

from libsnek.math import rms
from . import nokillsnek, hungry, claustrophobic


HEURISTICS = (
    # name, function, weight
    ("nokill", nokillsnek, 10.0),
    ("hungry", hungry, 1.0),
    ("claustrophobic", claustrophobic, 2.0),
)


def apply(board_state):
    weight_array = [
        weight * np.array(heuristic.apply(board_state))
        for name, heuristic, weight in HEURISTICS
    ]

    print(weight_array)

    return [
        rms(weights)
        for weights in zip(*weight_array)
    ]
