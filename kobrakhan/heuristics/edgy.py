from libsnek.movement import surroundings


def is_along_wall(board_state, pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2

    if x1 == x2 == 0:
        return True
    elif x1 == x2 == board_state.width:
        return True
    elif y1 == y2 == 0:
        return True
    elif y1 == y2 == board_state.height:
        return True

    return False


def score_move(board_state, pos1, pos2):
    if is_along_wall(board_state, pos1, pos2):
        return 0.0
    else:
        return 1.0


async def apply(board_state):
    my_pos = board_state.you.head

    return [
        score_move(board_state, my_pos, p)
        for p in surroundings(my_pos)
    ]
