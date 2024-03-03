from enum import Enum


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
    def __init__(self, game_id: int, status: GameStatus, created_at: int, winner_id: str | None):
        self.game_id = game_id
        self.status = status
        self.created_at = created_at
        self.winner_id = winner_id


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
