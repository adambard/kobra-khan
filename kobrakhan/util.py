from libsnek.movement import find_path_pred


def distance_to_nearest_food(board_state, start_pos):
    foods = set(board_state.food)

    if start_pos in foods:
        return 0

    path = find_path_pred(board_state, start_pos, lambda pos: pos in foods)

    if path is None:
        return 1000

    return len(path)

