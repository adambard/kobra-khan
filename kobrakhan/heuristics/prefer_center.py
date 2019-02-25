from libsnek.movement import distance, surroundings


async def apply(board_state):
    my_pos = board_state.you.head
    center_point = ((board_state.width / 2), (board_state.height / 2))
    reference_distance = float(distance((0, 0), center_point))

    return [
        max(0., (reference_distance - distance(pos, center_point)) / reference_distance)
        for pos in surroundings(my_pos)
    ]

