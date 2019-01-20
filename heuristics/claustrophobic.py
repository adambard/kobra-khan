from libsnek.movement import is_safe, surroundings
from libsnek.math import normalize_max


def fill_size(board_state, start_pos):
    """
    Return the number of squares that can be reached from this position
    """

    visited = set([start_pos])
    queue = set(p for p in surroundings(start_pos) if is_safe(board_state, p))
    cur_size = len(visited)

    while len(queue) > 0:
        for node in list(queue):
            for p in surroundings(node):
                if is_safe(board_state, p) and p not in visited:
                    queue.add(p)

            cur_size += 1
            visited.add(node)
            queue.remove(node)

    return cur_size



def apply(board_state):
    my_pos = board_state.you.body[0]

    return normalize_max(
        [fill_size(board_state, p) for p in surroundings(my_pos)]
    )
