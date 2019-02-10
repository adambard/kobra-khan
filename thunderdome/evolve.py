
# Interface with the battlesnake engine
import requests
import random
import itertools

from engine import GameEngine
from logger import SessionLogger


FOOD = 10
WIDTH = 17
HEIGHT = WIDTH


# Control just runs the default weights
CONTROL_SNAKES = [
    "http://localhost:9001",
    #"http://localhost:8003",
    #"http://localhost:8002",
]

# These snakes will be updated freely with different weights
CANDIDATE_POOL = [
    "http://localhost:8001",
    #"http://localhost:8002",
]

# Species: Initial weights for several different broad snake strategies.
SPECIES = [

    # Feb 10, morning
    {'nokill': 10.0, 'hungry': 0.009599704624897698, 'greedy': 0.006138126788865565, 'claustrophobic': 1.865062914461885, 'chase_tail': 0.0016779115607381168, 'food_control': 0.6660115727366539, 'fearful': 0.007058884129420791, 'prefer_center': 0.053705909932669424, 'trap': 0.33304324329008295},

    # An aggressive basis
    {
        'nokill': 10.0,
        "hungry": 0.0,
        "greedy": 0.1,
        "claustrophobic": 0.2,
        "chase_tail": 0.0,
        "food_control": 1.0,
        "fearful": 0.3,
        "prefer_center": 0.01,
        'trap': 0.3,
    },

    # Feb 9, evening
    {'nokill': 10.0, 'hungry': 0.014944712675957218, 'greedy': 0.012885576832539714, 'claustrophobic': 0.9278975012646877, 'chase_tail': 0.0017112611002428426, 'food_control': 1.442406066232509, 'fearful': 0.00739537338716581, 'prefer_center': 0.06317339564896189, 'trap': 0.27048823814612155},

    # Feb 9
    {'nokill': 10.0, 'hungry': 0.02355422930712964, 'greedy': 0.009232360014286196, 'claustrophobic': 1.2111120848918535, 'chase_tail': 0.0026448307302976252, 'food_control': 1.487004160153045, 'fearful': 0.004639027365583571, 'prefer_center': 0.03295525211382676, 'trap': 0.2750963279459166},

    # Evolved competitor, 1v1
    {'nokill': 10.0,
    'hungry': 0.03327219839040242,
    'greedy': 0.047222514766397154,
    'claustrophobic': 0.7937020681665596,
    'chase_tail': 0.01897738620160784,
    'food_control': 0.878449261712045,
    'fearful': 0.0031458442778517005,
    'prefer_center': 0.06402713660362136,
    'trap': 0.1,
    },

    #  controlling snake
    {'nokill': 10.0,
        'hungry': 0.04059474494039072,
        'greedy': 0.03703776128116555,
        'claustrophobic': 0.6631913081908803,
        'chase_tail': 0.005384366227868945,
        'food_control': 1.2727071297129864,
        'fearful': 0.002372517882311318,
        'prefer_center': 0.049015139133432285,
        'trap': 0.14950903183320732},

    # Am evolved scared sort of snake
    {'nokill': 10.0,
        'hungry': 0.1338427014684354,
        'greedy': 0.01,
        'claustrophobic': 0.23287877103283366,
        'chase_tail': 0.10320885300328839,
        'food_control': 0.01,
        'fearful': 0.336587063661696,
        'prefer_center': 0.0026805512203269396,
        'trap': 0.002820612769384502},
    # A scared sort of snake
    {
        'nokill': 10.0,
        "hungry": 0.1,
        "greedy": 0.0,
        "claustrophobic": 0.4,
        "chase_tail": 0.1,
        "food_control": 0.0,
        "fearful": 0.3,
        "prefer_center": 0.01,
        'trap': 0.01,
    },

    # An aggressive variety
    {
        'nokill': 10.0,
        "hungry": 0.0,
        "greedy": 0.1,
        "claustrophobic": 0.2,
        "chase_tail": 0.0,
        "food_control": 1.0,
        "fearful": 0.3,
        "prefer_center": 0.01,
        'trap': 0.3,
    },
]

"""
After running for ~20 hours:

# Scaredy snake:
{'nokill': 10.0,
 'hungry': 0.1 => 0.10817414553659199, 
 'greedy': 0.0 => 0.0,
 'claustrophobic': 0.4 => 0.6815991540373825,
 'chase_tail': 0.1 => 0.19417414778878947,
 'food_control': 0.0 => 0.0,
 'fearful': 0.3 => 0.36582308756415133
}

# Aggro snake:
{'nokill': 10.0,
 'hungry': 0.0 => 0.0,
 'greedy': 0.1 => 0.0574348272331993,
 'claustrophobic': 0.2 => 0.1872912501684063,
 'chase_tail': 0.0 => 0.0,
 'food_control': 1.0 => 1.6602421609353903,
 'fearful': 0.3 => 0.3227872704918379
 })

# Balanced snake:
{'nokill': 10.0,
 'hungry': 0.1 => 0.15441009947855308,
 'greedy': 0.07 => 0.11499722758018041,
 'claustrophobic': 0.4 => 0.5389925302697001,
 'chase_tail': 0.04 => 0.08989644185658045,
 'food_control': 0.3 => 0.2898573759519129,
 'fearful': 0.0 => 0.0})
"""


# Feb. 7 winner
"""
{'nokill': 10.0,
 'hungry': 0.1 => 0.03327219839040242,
 'greedy': 0.07 => 0.047222514766397154,
 'claustrophobic': 0.4 => 0.7937020681665596,
 'chase_tail': 0.04 => 0.01897738620160784,
 'food_control': 0.3 => 0.878449261712045,
 'fearful': 0.01 => 0.0031458442778517005,
 'prefer_center': 0.01 => 0.06402713660362136
}
"""


def jitter(num, damping=0.25):
    # damping = 0.5 -> 0.75 - 1.25x
    # damping = 0.25 -> 0.875 - 1.125x)
    factor = 1 + (damping * (random.random() - 0.5))  # daming 0.75 to 1.25
    return num * factor


def jitter_weights(weights):
    new_weights = {k: jitter(v) for k, v in weights.items()}
    new_weights['nokill'] = 10.0
    return new_weights


class GenetiSnake:
    def __init__(self, url, weights):
        self.url = url
        self.weights = weights

    def update_weights(self, weights):
        self.weights = weights
        requests.post(self.url + "/set_weights", json={
            "weights": weights
        })

    def adapt(self, weights):
        self.update_weights(jitter_weights(weights))

    def __repr__(self):
        return "GenetiSnake(url={}, weights={})".format(self.url, self.weights)


class EvolutionController:
    def __init__(self):

        self.species = SPECIES.copy()

        species = itertools.cycle(SPECIES)

        # Init weights with
        self.snakes = [
                GenetiSnake(url, weights) for url, weights in zip(CANDIDATE_POOL, species)
        ]


    def exercise(self, candidate, num_generations=10, round_size=10, num_offspring=3,
                 food=10, width=13, height=13):
        # Exercise each candidate in an all vs all match

        logger = SessionLogger()

        engine = GameEngine(CONTROL_SNAKES + [snake.url for snake in self.snakes], logger,
                            food=food, width=width, height=height)

        try:
            print("######## Starting Exercise ########")
            print("Exercising: %r" % candidate)
            for ii in range(num_generations):
                print("----- Generation {} -----".format(ii))

                logger.start_round("Round %d" % ii, self.snakes)

                best_score = 0
                best_weights = candidate.weights

                # Try <num_offspring> candidates per generation
                weight_options = [candidate.weights] + [
                    jitter_weights(candidate.weights) for _ in range(num_offspring)
                ]

                for weights in weight_options:
                    candidate.update_weights(weights)
                    scores = engine.run_round(round_size)
                    candidate_score = scores.get(candidate.url, 0)

                    print(weights)
                    print(" => ", candidate_score)

                    if candidate_score > best_score:
                        best_weights = weights
                        best_score = candidate_score

                print("Best: ", best_weights)

                candidate.update_weights(best_weights)

                logger.log_round_winner(candidate)

            print("######### Exercise complete ###########")
            print("")
            print("Winner: ", candidate.weights)

        finally:
            logger.dump()


    def snake_by_url(self, url):
        for s in self.snakes:
            if s.url == url:
                return s
        return None

    def log_state(self):
        for snake in self.snakes:
            print("%r" % snake)


if __name__ == "__main__":
    m = EvolutionController()

    while True:
        # Continuously evolve each species one at a time
        for s in m.snakes:
            m.log_state()
            m.exercise(s, round_size=29, num_generations=1, num_offspring=4,
                       food=FOOD, height=HEIGHT, width=WIDTH)
