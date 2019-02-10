import json
from datetime import datetime

from util import frequencies


class SessionLogger:
    def __init__(self):
        self.rounds = []

    def initialize(self):
        self.rounds = []

    def dump(self):
        log_file_name = datetime.now().strftime("logs/%Y%m%d_%H%M_results.json")
        with open(log_file_name, "w") as f:
            f.write(json.dumps(self.rounds))

    def start_round(self, round_name, candidates):
        print("===========================")
        print("Running round: %s" % round_name)

        self.rounds.append({
            "name": round_name,
            "candidates": [
                repr(s) for s in candidates
            ],
            "winner": None,
            "games": []
        })

    def log_round_winner(self, winner):
        r = self.rounds[-1]
        r['winner'] = repr(winner)
        r['scores'] = frequencies(r['games'])

        print("---- Round complete ----")
        for k, v in r['scores'].items():
            print("%s: %s" % (k, v))

        print()
        print("Winner: %r" % winner)
        print("===========================")

    def log_game(self, game_winner):
        self.rounds[-1]['games'].append(repr(game_winner))

