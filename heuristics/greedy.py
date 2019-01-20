from typing import List

from libsnek.movement import surroundings, find_path_pred
from libsnek.math import normalize_min


def distance_to_nearest_food(board_state, start_pos):
    foods = set(board_state.food)

    if start_pos in foods:
        return 0

    path = find_path_pred(board_state, start_pos, lambda pos: pos in foods)

    if path is None:
        return 1000

    return len(path)


async def apply(board_state) -> List[float]:
    my_pos = board_state.you.body[0]

    distances = [distance_to_nearest_food(board_state, p) for p in surroundings(my_pos)]

    return normalize_min(distances)
