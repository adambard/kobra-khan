from typing import List

from libsnek.movement import is_safe, surroundings


def apply(board_state) -> List[float]:
    my_pos = board_state.you.body[0]

    return [
        1.0 if is_safe(board_state, pos) else 0
        for pos in surroundings(my_pos)
    ]
