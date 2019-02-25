import functools
import numpy as np

from libsnek.math import normalize_max
from libsnek import movement


find_path = functools.lru_cache(maxsize=128)(movement.find_path)


@functools.lru_cache(maxsize=128, typed=False)
def controlled_by_us(board_state, my_pos, pos):
    if my_pos == pos:
        return True

    if not movement.is_ok(board_state, pos):
        return False

    my_path = find_path(board_state, my_pos, pos)
    if my_path is None:
        return False

    my_distance = len(my_path)

    for s in board_state.other_snakes:
        their_board = board_state.as_snake(s)
        their_pos = s.head

        their_path = find_path(their_board, their_pos, pos)
        if their_path is None:
            continue

        their_distance = len(their_path)
        if their_distance <= my_distance:
            return False

    return True


def control_zone_size(board_state, pos):
    if not movement.is_ok(board_state, pos):
        return 0

    board_size = board_state.width * board_state.height
    if board_size < 100:
        my_points = movement.flood_fill(board_state, pos, pred=lambda bs, p: controlled_by_us(bs, pos, p))
    elif board_size < 200:
        # Subsample the board by 2
        my_points = [
            (ii * 2, jj * 2)
            for ii in range(board_state.width // 2)
            for jj in range(board_state.height // 2)
            if controlled_by_us(board_state, pos, (ii * 2, jj * 2))
        ]
    else:
        # Subsample the board by 3 to improve performance
        my_points = [
            (ii * 3, jj * 3)
            for ii in range(board_state.width // 3)
            for jj in range(board_state.height // 3)
            if controlled_by_us(board_state, pos, (ii * 3, jj * 3))
        ]
    return len(my_points)



async def apply(board_state):
    options = [
        control_zone_size(board_state, pos)
        for pos in movement.surroundings(board_state.you.head)
    ]

    best_option = max(options)

    if best_option == 0:
        return np.array([0., 0., 0., 0.])
    else:
        return normalize_max(options)
