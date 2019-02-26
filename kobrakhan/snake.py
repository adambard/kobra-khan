import time
import logging
import numpy as np

from libsnek.math import rms
from .heuristics import (
    nokillsnek,
    hungry,
    claustrophobic,
    greedy,
    chase_tail,
    food_control,
    fearful,
    prefer_center,
    trap,
    voronoi,
    anorexic,
)


logger = logging.getLogger(__name__)



# Feb. 7
_HEURISTICS = (
    ("nokill", nokillsnek, (10.0, 0.0, 0.0)),
    ("hungry", hungry, (0.1, 0.0, 0.0)),
    ("greedy", greedy, (0.0, 0.0, 0.0)),
    ("claustrophobic", claustrophobic, (2.5, 0.0, 0.0)),
    ("chase_tail", chase_tail, (0.05, 0.0, 0.0)),
    ("food_control", food_control, (2.0, 0.0, 0.0)),
    ("fearful", fearful, (0.0, 0.0, 0.0)),
    ("prefer_center", prefer_center, (0.1, 0.0, 0.0)),
    ("trap", trap, (3.5, 0.0, 0.0)),
)

_HEURISTICS = (
    'nokill', nokillsnek, [10.0, 0.0, 0.0],
    'hungry', hungry, [0.005369300678086843, 0.003268013640785883, 1.7813380081496912e-05],
    'greedy', greedy, [0.009362001358854012, 0.011645957379055463, 0.006005531309176402],
    'claustrophobic', claustrophobic, [0.6269480634577916, 2.2012031339460205, 0.8754179668482581],
    'chase_tail', chase_tail, [0.000556725710925496, 0.0001956462204289212, 0.0008886035712730635],
    'food_control', food_control, [0.6942226445829581, 0.5810757995692893, 0.3327268315002361],
    'fearful', fearful, [0.01664651779346509, 0.019617527126630535, 0.007176081928688685],
    'prefer_center', prefer_center, [0.048333141628794096, 0.052060764367102386, 0.03563491380500378],
    'trap', trap, [0.13631799841086253, 0.07130229273502012, 0.9064453594593518]
)

# Feb 14 optimizations
_HEURISTICS = (
        ('nokill', nokillsnek, [10.0, 0.0, 0.0]),
        ('hungry', hungry, [2.59060974, 3.54111293, 4.62038812]),
        ('greedy', greedy, [1.21827769, 3.30713357, 3.21617125]),
        ('claustrophobic', claustrophobic, [4.73544136, 2.70753575, 3.27694413]),
        ('chase_tail', chase_tail, [3.4946728, 3.93677021, 1.54745589]),
        ('food_control', food_control, [3.15212141, 3.87226717, 0.1555264]),
        ('fearful', fearful, [1.26572758, 2.00172861, 4.36370224]),
        ('prefer_center', prefer_center, [2.47315743, 0.41899597, 4.81262515]),
        ('trap', trap, [4.88261546, 3.99515451, 2.73392744]),
)
 

# Feb 17 results
_HEURISTICS = (
    ('nokill', nokillsnek, [10.0, 0.0, 0.0]),
    ('hungry', hungry, [0.23350878, 0.22916532, 0.69952455]),
    ('greedy', greedy, [0.02814266, 0.95264534, 0.25091182]),
    ('claustrophobic', claustrophobic, [4.82115927, 2.08009261, 3.68012842]),
    ('chase_tail', chase_tail, [0.81450637, 0.55973576, 0.60448506]),
    ('food_control', food_control, [3.10951646, 0.95021503, 4.98660824]),
    ('fearful', fearful, [0.14547697, 0.39218828, 0.2132348]),
    ('prefer_center', prefer_center, [0.18180493, 0.01355381, 0.65896626]),
    ('trap', trap, [4.09536908, 2.3474821, 1.60712454]),
    ('voronoi', voronoi, [3.10951646, 0.95021503, 4.98660824]),
    ('anorexic', anorexic, [0.2, 0.0, 0.0]),
)

# Feb 24 most refined
_HEURISTICS = (
    ('nokill', nokillsnek, [10.0, 0.0, 0.0]),
    ('hungry', hungry, [0.25725192, 0.75612221, 0.36928885,]),
    ('greedy', greedy, [0.1217629,  0.6143386,  0.70539159,]),
    ('claustrophobic', claustrophobic, [3.28527238, 0.55693352, 2.60936894,]),
    ('chase_tail', chase_tail, [0.04495929, 0.27770769, 0.95049992,]),
    ('food_control', food_control, [2.14628304, 0.55291096, 2.21946986,]),
    ('fearful', fearful, [0.13204319, 0.37183544, 1.0]),
    ('prefer_center', prefer_center, [0.48035746, 0.76618417, 0.19014682,]),
    ('trap', trap, [4.33381386, 3.20958668, 3.97291225,]),
    ('voronoi', voronoi, [3.33009104, 2.61055774, 0.8357004,]),
    ('anorexic', anorexic, [0.19681902, 0.10967602, 0.1025919,]),
)

# Feb 25 most refined
HEURISTICS = (
    ('hungry', hungry, [0.30812111, 0.68373428, 0.44728139,]),
    ('greedy', greedy, [0.11229443, 0.02941391, 1.42036349,]),
    ('claustrophobic', claustrophobic, [3.34177219, 0.57054492, 3.15855432,]),
    ('chase_tail', chase_tail, [0.03420051, 0.32551665, 0.89777061,]),
    ('food_control', food_control, [2.1978414,  0.59805776, 2.1631654,]),
    ('fearful', fearful, [0.1220004,  0.44553593, 0.30066594,]),
    ('prefer_center', prefer_center, [0.47036855, 0.73791454, 0.21458924,]),
    ('trap', trap, [4.65002321, 3.10868752, 4.10371105,]),
    ('voronoi', voronoi, [2.92269436, 2.94117605, 0.91644012,]),
    ('anorexic', anorexic, [0.0, 0.0, 0.0,]),
)



def log_weights():
    logger.debug("---- Running with weights ----")
    for (name, _, weights) in HEURISTICS:
        logger.debug(f"{name:20s}: {weights}")
    logger.debug("------------------------------")


log_weights()


def set_weights(new_weights):
    """
    Update the weights in HEURISTICS to new ones
    """
    global HEURISTICS
    HEURISTICS = [
        (name, impl, new_weights.get(name, weight))
        for name, impl, weight in HEURISTICS
    ]
    log_weights()


def compute_weight(board_state, coefficients):
    dimensions = np.array([1., board_state.turn / 500., len(board_state.snakes) / 8.])
    return np.sum(dimensions * coefficients)


async def apply(board_state):
    global HEURISTICS

    future_weights = [
        (compute_weight(board_state, coefficients), heuristic.apply(board_state))
        for _name, heuristic, coefficients in HEURISTICS
    ]

    weight_array = [
        weight * np.array(await future)
        for weight, future in future_weights
    ]

    return [
        rms(weights)
        for weights in zip(*weight_array)
    ]

