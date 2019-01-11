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

def move(pos, d):
    if d == "u":
        return {"x": pos["x"], "y": pos["y"] - 1}
    elif d == "r":
        return {"x": pos["x"] + 1, "y": pos["y"]}
    elif d == "d":
        return {"x": pos["x"], "y": pos["y"] + 1}
    elif d == "l":
        return {"x": pos["x"] - 1, "y": pos["y"]}
    else:
        return pos

def surroundings(pos):
    return [
        move(pos, "u"),
        move(pos, "r"),
        move(pos, "d"),
        move(pos, "l"),
    ]


def is_safe(board_state, pos):
    print("safe?", pos)
    if pos["x"] < 0:
        return False
    elif pos["x"] >= board_state["board"]["width"]:
        return False
    elif pos["y"] < 0:
        print("Unsafe")
        return False
    elif pos["y"] >= board_state["board"]["height"]:
        return False

    for snake in board_state["board"]["snakes"]:
        if pos in snake["body"][:-1]:
            return False

    print("Ye")
    return True


def apply(board_state):
    my_pos = board_state["you"]["body"][0]

    return [
        1 if is_safe(board_state, pos) else 0
        for pos in surroundings(my_pos)
    ]
