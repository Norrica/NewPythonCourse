from enum import Enum

import requests


class GameStatus(Enum):
    NEW = 0
    ACTIVE = 1
    FINISHED = 2


class User:
    def __init__(self, user_id: str, tg_id: int, username: str):
        self.user_id = user_id
        self.tg_id = tg_id
        self.username = username


class GameUser:
    def __init__(self, user_id: str, username: str, sign: str):
        self.user_id = user_id
        self.username = username
        self.sign = sign


class Game:
    def __init__(self, game_id: int, status: GameStatus, created_at: int):
        self.game_id = game_id
        self.status = status
        self.created_at = created_at


class Move:
    def __init__(self, move_id: int, game_id: int, user_id: str, row: int, col: int, sign: str, created_at: int):
        self.move_id = move_id
        self.game_id = game_id
        self.user_id = user_id
        self.row = row
        self.col = col
        self.sign = sign
        self.created_at = created_at


class Rating:
    def __init__(self, username: str, wins: int):
        self.username = username
        self.wins = wins



class HttpClient:
    def __init__(self):
        self.url = "http://141.147.57.10:8080"

    def ping(self) -> bool:
        try:
            response = requests.get(f"{self.url}/ping").json()
            return response["status"] == 200
        except:
            return False

    def get_user(self, user_id: str) -> User | None:
        response = requests.get(f"{self.url}/get_user?user_id={user_id}").json()
        if response["status"] != 200:
            return None

        return User(**response["body"]["user"])

    def get_active_game_by_user_id(self, user_id: str) -> tuple[Game, list[GameUser], list[Move]] | None:
        response = requests.get(f"{self.url}/get_active_game_by_user_id?user_id={user_id}").json()
        if response["status"] != 200:
            return None

        return Game(**response["body"]["game"]), [GameUser(**user) for user in response["body"]["users"]], [Move(**move)
                                                                                                            for move in
                                                                                                            response[
                                                                                                                "body"][
                                                                                                                "moves"]]

    def join_game(self, user_id: str) -> tuple[Game, list[GameUser]] | None:
        response = requests.get(f"{self.url}/join_game?user_id={user_id}").json()
        if response["status"] != 200:
            return None

        print(response)
        return Game(**response["body"]["game"]), [GameUser(**user) for user in response["body"]["users"]]

    def get_game_info(self, game_id: int) -> tuple[Game, list[GameUser], list[Move]] | None:
        response = requests.get(f"{self.url}/get_game_info?game_id={game_id}").json()
        if response["status"] != 200:
            return None

        return Game(**response["body"]["game"]), [GameUser(**user) for user in response["body"]["users"]], [Move(**move)
                                                                                                            for move in
                                                                                                            response[
                                                                                                                "body"][
                                                                                                                "moves"]]

    def make_move(self, user_id: str, game_id: int, row: int, col: int, sign: str) -> Move | None:
        response = requests.get(
            f"{self.url}/make_move?user_id={user_id}&game_id={game_id}&row={row}&col={col}&sign={sign}").json()
        if response["status"] != 200:
            return None

        return Move(**response["body"]["move"])

    def get_rating(self) -> list[Rating] | None:
        response = requests.get(f"{self.url}/get_rating").json()
        if response["status"] != 200:
            return None

        return [Rating(**rating) for rating in response["body"]["rating"]]


