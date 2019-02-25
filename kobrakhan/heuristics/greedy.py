from typing import List

from ..util import distance_to_nearest_food

from libsnek.movement import surroundings
from libsnek.math import normalize_min




async def apply(board_state) -> List[float]:
    my_pos = board_state.you.body[0]

    distances = [distance_to_nearest_food(board_state, p) for p in surroundings(my_pos)]

    return normalize_min(distances)
