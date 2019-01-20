from libsnek.movement import is_safe, surroundings, flood_fill
from libsnek.math import normalize_max


def fill_size(board_state, start_pos):
    """
    Return the number of squares that can be reached from this position
    """

    if not is_safe(board_state, start_pos, max_depth=1):
        return 0

    # 10% of the board area is plenty
    threshold = board_state.width * board_state.height / 10

    return len(flood_fill(board_state, start_pos, threshold=threshold))


async def apply(board_state):
    my_pos = board_state.you.body[0]

    fill_sizes = [fill_size(board_state, p) for p in surroundings(my_pos)]

    try:
        return normalize_max(fill_sizes)
    except ZeroDivisionError:
        print("Error computing fill size", fill_sizes)
        return [0., 0., 0., 0.]
