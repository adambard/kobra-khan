import os
import re
import json
from pprint import pprint

import numpy as np
from matplotlib import pyplot

"""
[
  {
    "name": "Round 0",
    "candidates": [
      "GenetiSnake(url=http://localhost:8001, weights={'nokill': 10.0, 'hungry': 0.031331223570747045, 'greedy': 0.022026325414957516, 'claustrophobic': 0.7350592826350633, 'chase_tail': 0.0075290141094072486, 'food_control': 0.8310963602724599, 'fearful': 0.0028931965530780385, 'prefer_center': 0.08160095502122515, 'trap': 0.07716781894465874})"
    ],
    "winner": "GenetiSnake(url=http://localhost:8001, weights={'nokill': 10.0, 'hungry': 0.03610982851382496, 'greedy': 0.024462531382815775, 'claustrophobic': 0.7060437203403923, 'chase_tail': 0.006313391995510394, 'food_control': 0.8466009274322388, 'fearful': 0.003012630423241906, 'prefer_center': 0.062388213993467216, 'trap': 0.07050277991844925})",
    "games": [
      "'http://localhost:9001'",
      "'http://localhost:9001'",
      ...

      "'http://localhost:9001'",
      "'http://localhost:8001'"
    ],
    "scores": {
      "'http://localhost:9001'": 64,
      "'http://localhost:8001'": 78,
      "None": 3
    }
  }
]
"""

MATCH_FILENAME = re.compile("20190209_\d{4}_results.json")


HEURISTICS = ["hungry", "greedy", "claustrophobic", "chase_tail", "food_control", "fearful", "prefer_center", "trap"]
ZERO = [np.nan for _ in HEURISTICS]


SNAKE_RE = re.compile(
    r"GenetiSnake\(url=(?P<url>[^,]+), weights={'nokill': (?P<nokill>\d+.?\d*), 'hungry': (?P<hungry>\d+.?\d*), 'greedy': (?P<greedy>\d+.?\d*), 'claustrophobic': (?P<claustrophobic>\d+.?\d*), 'chase_tail': (?P<chase_tail>\d+.?\d*), 'food_control': (?P<food_control>\d+.?\d*), 'fearful': (?P<fearful>\d+.?\d*), 'prefer_center': (?P<prefer_center>\d+.?\d*), 'trap': (?P<trap>\d+.?\d*).*"
)

def get_snake_weights(s):
    if not s:
        return ZERO

    m = SNAKE_RE.match(s)
    if not m:
        return ZERO

    try:
        weights = np.array([float(m.group(k)) for k in HEURISTICS])

        # Weights relativee to claustrophobic
        return weights / weights[2]
    except IndexError:
        print(k, m.groupdict())
        raise


def get_round_scores(r):
    try:
        scores = r["scores"]
        return [scores.get("'http://localhost:8001'", None), scores.get("'http://localhost:9001'", None)]
    except KeyError:
        return (None, None)


def plot_round_scores(scores):
    pyplot.plot(scores[0, :, 0], 'o')
    pyplot.plot(scores[0, :, 1], 'x')
    pyplot.show()



def plot_weights(weights):

    weights = np.array([
        get_snake_weights(r['winner']) for r in rounds
    ])

    SYMBOLS = ['.', '^', 's', '+', 'o', '.', 'x', '.', '.', '.']

    for ii in range(7):
        pyplot.plot(weights[:, ii], SYMBOLS[ii], label=HEURISTICS[ii])

    pyplot.show()



rounds = []
for fn in sorted(os.listdir(".")):
    if MATCH_FILENAME.match(fn):
        with open(fn) as f:
            print("Adding", fn, "to rounds")
            rounds += json.load(f)


scores = np.array([map(get_round_scores, rounds)])
plot_round_scores(scores)


