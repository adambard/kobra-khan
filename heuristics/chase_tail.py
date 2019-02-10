from libsnek.movement import surroundings, find_path

def distance_to_tail(board_state, pos):
    tail = board_state.you.body[-1]
    path = find_path(board_state, pos, tail)
    if path:
        return len(path)
    return 9999


async def apply(board_state):
    head = board_state.you.body[0]

    return [1./ distance_to_tail(board_state, p) for p in surroundings(head)]

