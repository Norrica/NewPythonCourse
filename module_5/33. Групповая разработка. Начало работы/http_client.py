import threading

import requests

from models import User, Game, GameUser, Move, Rating


def run_in_thread(func):
    def wrapper(*args, **kwargs):
        result_container = {"result": None}
        thread = threading.Thread(target=lambda: result_container.update(result=func(*args, **kwargs)))
        thread.start()
        return result_container["result"]
    return wrapper


class HttpClient:
    def __init__(self):
        self.url = "https://deeppythontestasd.pythonanywhere.com"

    def ping(self) -> bool:
        response = requests.get(f"{self.url}/ping").json()
        return response["status"] == 200

    def get_user(self, user_id: str) -> User | None:
        try:
            response = requests.get(f"{self.url}/get_user?user_id={user_id}").json()
            if response["status"] != 200:
                return None

            return User(**response["body"]["user"])
        except:
            return None

    def get_active_game_by_user_id(self, user_id: str) -> tuple[Game, list[GameUser], list[Move]] | None:
        try:
            response = requests.get(f"{self.url}/get_active_game_by_user_id?user_id={user_id}").json()
            if response["status"] != 200:
                return None

            game = Game(**response["body"]["game"])
            users = [GameUser(**user) for user in response["body"]["users"]]
            moves = [Move(**move) for move in response["body"]["moves"]]

            return game, users, moves
        except:
            return None

    def join_game(self, user_id: str) -> tuple[Game, list[GameUser]] | None:
        try:
            response = requests.get(f"{self.url}/join_game?user_id={user_id}").json()
            if response["status"] != 200:
                return None

            game = Game(**response["body"]["game"])
            users = [GameUser(**user) for user in response["body"]["users"]]

            return game, users
        except:
            return None

    def get_game_info(self, game_id: int) -> tuple[Game, list[GameUser], list[Move]] | None:
        try:
            response = requests.get(f"{self.url}/get_game_info?game_id={game_id}").json()
            if response["status"] != 200:
                return None

            game = Game(**response["body"]["game"])
            users = [GameUser(**user) for user in response["body"]["users"]]
            moves = [Move(**move) for move in response["body"]["moves"]]

            return game, users, moves
        except:
            return None

    @run_in_thread
    def make_move(self, user_id: str, game_id: int, row: int, col: int, sign: str) -> Move | None:
        try:
            response = requests.get(
                f"{self.url}/make_move?user_id={user_id}&game_id={game_id}&row={row}&col={col}&sign={sign}").json()
            if response["status"] != 200:
                return None

            return Move(**response["body"]["move"])
        except:
            return None

    def get_rating(self) -> list[Rating] | None:
        try:
            response = requests.get(f"{self.url}/get_rating").json()
            if response["status"] != 200:
                return None

            return [Rating(**rating) for rating in response["body"]["rating"]]
        except:
            return None

    def leave_game(self, user_id: str, game_id: str) -> bool:
        try:
            response = requests.get(f"{self.url}/leave_game?user_id={user_id}&game_id={game_id}").json()

            return response["status"] == 200
        except:
            return False
