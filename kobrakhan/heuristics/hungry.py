from typing import List

from ..util import distance_to_nearest_food
from libsnek.movement import surroundings
from libsnek.math import normalize_min


async def apply(board_state) -> List[float]:
    """
    Find the distance to the nearest food, but weight it by
    current hunger levels
    """
    my_pos = board_state.you.body[0]

    health_factor = (1.0 - (board_state.you.health / 100.0)) ** 4

    distances = [
        health_factor * distance_to_nearest_food(board_state, p)
        for p in surroundings(my_pos)
    ]

    return normalize_min(distances)
