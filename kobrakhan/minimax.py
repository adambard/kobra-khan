"""
A minimax layer that searches for significant outcomes (i.e. our death
or another snake's victory).
"""

import numpy as np
import functools

from enum import Enum
from util import distance_to_nearest_food
from libsnek.movement import is_ok, surroundings


MIN_SCORE = 0.001
MAX_SCORE = 9999
NEUTRAL_SCORE = 1


class Move(Enum):
    UP = "u"
    RIGHT = "r"
    DOWN = "d"
    LEFT = "l"

    @classmethod
    def as_word(cls, val):
        if val == cls.UP:
            return "up"
        elif val == cls.RIGHT:
            return "right"
        elif val == cls.DOWN:
            return "down"
        else:
            return "left"


@functools.lru_cache(maxsize=128, typed=False)
def is_dead(board_state, pos=None):

    if pos is None:
        pos = board_state.you.head

    x, y = pos
    if x < 0 or y < 0:
        return True
    elif x > board_state.width or y > board_state.height:
        return True

    if board_state.you.health <= distance_to_nearest_food(board_state, pos):
        print("POOR HEALTH", distance_to_nearest_food(board_state, pos))
        return True

    for s in board_state.other_snakes:
        if pos in s.body[1:-1]:
            return True
        elif pos == s.tail:
            return any(p in board_state.food for p in surroundings(s.head))
        elif pos == s.head:
            return len(s.body) >= len(board_state.you.body)

    return False


def score_board_state(board_state):
    """
    If we've died, return MIN_SCORE
    If we've won, return MAX_SCORE
    Otherwise, return 0
    """
    if is_dead(board_state):
        return MIN_SCORE

    all_others_dead = True
    num_dead = 0
    for s in board_state.other_snakes:
        bs = board_state.as_snake(s)
        if is_dead(bs):
            num_dead += 1
        else:
            all_others_dead = False

    if all_others_dead:
        return MAX_SCORE

    return NEUTRAL_SCORE


def minimax_nodes(board_state):
    """Return a set of board states representing moves in each valid direction"""

    return [
        board_state.as_snake(board_state.you, with_move=pos)
        for pos in surroundings(board_state.you.head)
        if not is_dead(board_state, pos)
    ]


async def minimax_score(board_state, maximizing_player=True, depth=5):

    if depth == 0:
        return score_board_state(board_state)

    if maximizing_player:
        # Make our own best move
        score = MIN_SCORE
        for bs in minimax_nodes(board_state):
            score = max(score, await minimax_score(bs, False, depth - 1))

        return score

    else:
        # Make each other snake's move to minimize our score
        scores = []

        new_bs = board_state

        for s in board_state.other_snakes:
            min_score = MAX_SCORE

            for bs in minimax_nodes(new_bs.as_snake(s)):
                score = await minimax_score(bs.as_snake(board_state.you), True, depth - 1)
                if score < min_score:
                    min_score = score
                    new_bs = bs

            scores.append(min_score)

        return min(scores)


async def apply(board_state):
    positions = surroundings(board_state.you.head)

    out = []

    for pos, d in zip(positions, list(Move)):
        if is_dead(board_state, pos):
            out.append(MIN_SCORE)
        else:
            bs = board_state.as_snake(board_state.you, with_move=pos)
            out.append(await minimax_score(bs, True, depth=3))

    return np.array(out)

