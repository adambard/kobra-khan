"""
board_state:

    {
        "board": {
            "height",
            "width",
            "food": [
                {"x": int, "y": int}
            ],
            "snakes": [
                {"id",
                 "name",
                 "health",
                 body: [
                   {"x": int, "y": int},
                   ...
                 ]
                },
            ],
            "you": {
                {
                    "id",
                    "name",
                    "health",
                    "body": [
                        {"x": int, "y": int},
                        ...
                    ]
                }
            }
        }
    }

"""

from data import BoardState

def move(pos, d):
    x, y = pos
    if d == "u":
        return (x, y - 1)
    elif d == "r":
        return (x + 1, y)
    elif d == "d":
        return (x, y + 1)
    elif d == "l":
        return (x - 1, y)
    else:
        return pos

def surroundings(pos):
    return [
        move(pos, "u"),
        move(pos, "r"),
        move(pos, "d"),
        move(pos, "l"),
    ]


def is_safe(board_state: BoardState, pos):
    x, y = pos

    print("safe?", pos)
    if x < 0:
        return False
    elif x >= board_state.width:
        return False
    elif y < 0:
        print("Unsafe")
        return False
    elif y >= board_state.height:
        return False

    for snake in board_state.snakes:
        if pos in snake.body[:-1]:
            return False

    print("Ye")
    return True


def apply(board_state):
    my_pos = board_state.you.body[0]

    return [
        1 if is_safe(board_state, pos) else 0
        for pos in surroundings(my_pos)
    ]
