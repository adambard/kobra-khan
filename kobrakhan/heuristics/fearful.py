"""
Fearful: Attempt to maximize the distance between us and other snakes(' heads)
"""
from typing import List

from libsnek.movement import surroundings, find_path
from libsnek.math import normalize_max, rms
import numpy as np


def distance_to_snake(board_state, pos, snake):
    path = find_path(board_state, pos, snake.head)
    if path is None:
        # A rough "max" distance
        return board_state.width + board_state.height

    return len(path)


def snake_distance_rms(board_state, pos):
    d = np.array([
        float(distance_to_snake(board_state, pos, s))
        for s in board_state.other_snakes
    ])
    return rms(d)


async def apply(board_state) -> List[float]:
    my_pos = board_state.you.body[0]

    distances = [
        snake_distance_rms(board_state, p)
        for p in surroundings(my_pos)
    ]

    return normalize_max(distances)

