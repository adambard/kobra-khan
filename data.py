from pandas import *

def point_to_tuple(p):
    return (p["x"], p["y"])


class Snake(object):
    def __init__(self, raw_snake):
        self.raw = raw_snake

    @property
    def id(self):
        return self.raw["id"]

    @property
    def health(self):
        return self.raw["health"]

    @property
    def name(self):
        return self.raw["name"]

    @property
    def body(self):
        return [point_to_tuple(p) for p in self.raw["body"]]


class BoardState(object):

    def __init__(self, raw_board_state):
        self.raw = raw_board_state
        self.precalc = [['safe' for i in range(3)] for j in range(2)]
        # print(DataFrame(self.precalc))
        print('************')

    @property
    def you(self):
        return Snake(self.raw["you"])

    @property
    def width(self):
        return self.raw["board"]["width"]

    @property
    def height(self):
        return self.raw["board"]["height"]

    @property
    def food(self):
        return [point_to_tuple(p) for p in self.raw["board"]["food"]]

    @property
    def snakes(self):
        return [Snake(p) for p in self.raw["board"]["snakes"]]

    @property
    def state(self):
        for snake in self.raw["board"]["snakes"]:
            for body in snake['body']:
                x = body['x']
                y = body['y']
                self.precalc[y][x] = 'unsafe'
        return self.precalc
