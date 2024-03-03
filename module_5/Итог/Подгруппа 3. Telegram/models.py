class User:
    def __init__(self, user_id: str, tg_id: int, username: str):
        self.user_id = user_id
        self.tg_id = tg_id
        self.username = username


class Rating:
    def __init__(self, username: str, wins: int):
        self.username = username
        self.wins = wins
