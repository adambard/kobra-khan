from libsnek.movement import surroundings, flood_fill, distance, find_path_pred


# Only antagonize snakes that are at least this close
MAX_TARGET_DISTANCE = 6

# The maximum number of space an enemy snake can have
# where we still consider it "trappedd"
MAX_TRAP_SIZE = 10


def nearest_pathable_snake(board_state, pos):
    min_distance = MAX_TARGET_DISTANCE + 1
    nearest_snake = None
    for s in board_state.other_snakes:

        # Path length is never shorter than distance,
        # so don't waste time pathfinding in this case
        if distance(pos, s.head) >= min_distance:
            continue

        ps = surroundings(s.head)
        pred = lambda p: p in ps
        path = find_path_pred(board_state, pos, pred)

        if path is not None and len(path) < min_distance:
            nearest_snake = s
            min_distance = len(path)

    return nearest_snake


def antagonism_factor(board_state, snake, pos):
    """
    If our head were at position pos, how much space would this snake have?
    (less space = better)
    """
    their_board = board_state.as_snake(snake, with_move=pos)
    points = flood_fill(their_board, snake.head, threshold=MAX_TRAP_SIZE)

    # Set our head up
    return 1. / (1 + len(points))


async def apply(board_state):
    """
    For the nearest snake to which we have a path, attempt to trap it
    """
    my_pos = board_state.you.head
    target = nearest_pathable_snake(board_state, my_pos)

    if target is None:
        return [0., 0., 0., 0.]

    return [
        antagonism_factor(board_state, target, p)
        for p in surroundings(my_pos)
    ]

