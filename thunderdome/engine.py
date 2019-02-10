import json
import time
import requests
import logging

from util import frequencies


ENGINE_URL = "http://localhost:3005"



class GameEngine:

    def __init__(self, snake_urls, logger, food=10, width=13, height=13):
        self.snake_urls = snake_urls
        self.food = food
        self.width = width
        self.height = height

        self.logger = logger

    def run_round(self, n=1):
        return frequencies([
            self.run_game()
            for _ in range(n)
        ])

    def run_game(self):
        "Start a game, then watch it and return the winning snake"
        game_id = self.start_game()

        snake_urls = self.surviving_snakes(game_id)
        survivor_count = len(snake_urls) + 1

        while len(snake_urls) > 1:
            if survivor_count > len(snake_urls):
                survivor_count = len(snake_urls)

            # TODO: Sleep
            time.sleep(1)
            snake_urls = self.surviving_snakes(game_id)

        if len(snake_urls) == 1:
            winner = snake_urls[0]
            for url in self.snake_urls:
                if url == winner:
                    self.logger.log_game(url)
                    print("Game %s winner: %r" % (game_id, url))
                    return url

        self.logger.log_game(None)
        print("Game %s winner: Tie" % game_id)

        return None


    def start_game(self):
        url = ENGINE_URL + "/games"

        result = requests.post(url, json={
            "food": self.food,
            "width": self.width,
            "height": self.height,
            "snakes": [
                {"name": "snake-%d" % ii, "url": url}
                for ii, url in enumerate(self.snake_urls)
            ]
        })

        assert result.status_code == 200

        game_id = result.json().get("ID")

        resp = requests.post(url + "/" + game_id + "/start")
        assert resp.status_code == 200, repr(resp.content)

        return game_id

    def surviving_snakes(self, game_id):
        url = ENGINE_URL + "/games/" + game_id

        resp = requests.get(url)

        try:
            return [s["URL"] for s in resp.json()["LastFrame"]["Snakes"]
                    if s["Death"] is None]
        except json.JSONDecodeError:
            logging.exceeption("Error decoding engine response!")
            return []
