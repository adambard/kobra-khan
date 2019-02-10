from typing import List

from libsnek.movement import surroundings
from libsnek.math import normalize_min

from . import greedy


async def apply(board_state) -> List[float]:
    """
    Find the distance to the nearest food, but weight it by
    current hunger levels
    """
    my_pos = board_state.you.body[0]

    health_factor = board_state.you.health / 100.0

    distances = [
        (health_factor * greedy.distance_to_nearest_food(board_state, p))**2
        for p in surroundings(my_pos)
    ]

    return normalize_min(distances)
