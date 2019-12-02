from libsnek.math import normalize_min
from libsnek.movement import find_path_pred, find_path, surroundings, distance


def nearest_to_me(board_state, my_pos, food_pos):
    my_path = find_path(board_state, my_pos, food_pos)
    if my_path is None:
        return False

    for s in board_state.other_snakes:
        if distance(s.head, food_pos) > len(my_path):
            # Quickly exclude snakes that can't possibly be closer
            continue

        their_path = find_path(board_state.as_snake(s), s.head, food_pos)
        if their_path is None:
            continue

        if (len(their_path) - 1) <= len(my_path):
            return False

    return True


def distance_to_target_food(board_state, start_pos):
    foods = set(board_state.food)

    if start_pos in foods:
        return 0

    pred = lambda pos: pos in foods and nearest_to_me(board_state, start_pos, pos)

    path = find_path_pred(board_state, start_pos, pred)

    if path is None:
        return board_state.width + board_state.height

    return len(path)


async def apply(board_state):
    distances = [
        distance_to_target_food(board_state, p)
        for p in surroundings(board_state.you.head)
    ]

    print("OPPORTUNIST", distances)

    return normalize_min(distances)
