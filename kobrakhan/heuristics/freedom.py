import functools
from libsnek.math import rms, normalize_max
from libsnek.movement import surroundings, is_safe


@functools.lru_cache(maxsize=128, typed=False)
def freedom_rating(board_state, pos, depth=3):
    """
    Like minimax but with a static board. A quick guess at which
    direction has more options.
    """
    if not is_safe(board_state, pos, max_depth=1):
        return 0.0

    if depth == 0:
        free_points = len([
            p for p in surroundings(pos)
            if is_safe(board_state, p, max_depth=1)
        ])
        return free_points

    scores = [
        freedom_rating(board_state, p, depth=depth - 1)
        for p in surroundings(pos)
    ]
    if not scores:
        return 0.0
    return rms(scores)


async def apply(board_state):

    ratings = [
        freedom_rating(board_state, p)
        for p in surroundings(board_state.you.head)
    ]
    print("Freedom", ratings)

    return normalize_max(ratings)
