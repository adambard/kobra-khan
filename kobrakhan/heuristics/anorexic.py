from typing import List

from libsnek.movement import surroundings


async def apply(board_state) -> List[float]:
    """Simply avoid food"""

    return [
        0.0 if p in board_state.food else 1.0
        for p in surroundings(board_state.you.head)
    ]
