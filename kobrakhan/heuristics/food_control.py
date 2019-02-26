"""
This heuristic suggests a movement that controls the most food, i.e.
attempts to ensure that we're closer to the most food than any other
snake
"""

from typing import List


from libsnek.movement import surroundings, find_path, is_safe


def is_my_food(board_state, my_pos, food):
    my_path = find_path(board_state, my_pos, food)

    if my_path is None:
        return False

    for s in board_state.other_snakes:
        their_board = board_state.as_snake(s)
        their_path = find_path(their_board, s.head, food)

        if their_path is None:
            continue

        if len(their_path) <= len(my_path):
            return False

    return True


def food_count(board_state, pos):
    controlled_by_me = 0

    if not is_safe(board_state, pos):
        return 0

    for food in board_state.food:
        if is_my_food(board_state, pos, food):
            controlled_by_me += 1

    return controlled_by_me


async def apply(board_state) -> List[float]:
    num_food = len(board_state.food)
    if num_food < 1:
        return [0., 0., 0., 0.]

    ret = [
        food_count(board_state, p) / float(len(board_state.food))
        for p in surroundings(board_state.you.head)
    ]
    return ret
