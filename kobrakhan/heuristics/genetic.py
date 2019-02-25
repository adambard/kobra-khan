import numpy as np

from libsnek.math import rms
from . import (
    nokillsnek,
    hungry,
    claustrophobic,
    greedy,
    chase_tail,
    food_control,
    fearful,
    prefer_center,
    trap
)
import pprint


_HEURISTICS = (
    # name, function, weight
    ("nokill", nokillsnek, 10.0),
    ("hungry", hungry, 1.0),
    ("greedy", greedy, 0.5),
    ("claustrophobic", claustrophobic, 2.0),
    ("chase_tail", chase_tail, 1.0),
)

# Feb. 7
HEURISTICS = (
    ("nokill", nokillsnek, 10.0),
    ("hungry", hungry, 0.1),
    ("greedy", greedy, 0.0),
    ("claustrophobic", claustrophobic, 2.5),
    ("chase_tail", chase_tail, 0.05),
    ("food_control", food_control, 2.0),
    ("fearful", fearful, 0.0),
    ("prefer_center", prefer_center, 0.1),
    ("trap", trap, 3.5),
)

def print_weights():
    print("---- Running with weights ----")
    for (name, _, weight) in HEURISTICS:
        print(f"{name:20s}: {weight}")
    print("------------------------------")

print_weights()


def set_weights(new_weights):
    """
    Update the weights in HEURISTICS to new ones
    """
    global HEURISTICS
    HEURISTICS = [
        (name, impl, new_weights.get(name, weight))
        for name, impl, weight in HEURISTICS
    ]
    print_weights()


async def apply(board_state):
    global HEURISTICS

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
