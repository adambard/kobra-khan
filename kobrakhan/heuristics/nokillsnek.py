from typing import List

from libsnek.movement import is_safe, surroundings


def rating(board_state, pos):
    if is_safe(board_state, pos, max_depth=2):
        return 1.0
    # If nowhere is completely safe, try a less-cautious algorithm
    elif is_safe(board_state, pos, max_depth=1, check_edibility=False):
        return 0.5
    else:
        # Make a kamikaze attack if we have no other option
        for snake in board_state.snakes:
            if pos == snake.body[0]:
                return 0.1
    return 0.0


async def apply(board_state) -> List[float]:
    my_pos = board_state.you.body[0]

    return [
        rating(board_state, pos) for pos in surroundings(my_pos)
    ]
