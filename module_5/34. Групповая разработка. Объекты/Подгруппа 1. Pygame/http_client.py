import requests

from models import User, Game, Player, Move


class HttpClient:
    def __init__(self):
        self.host = "https://tictac.redko.us/"

    def get_user(self, user_id: str) -> User | None:
        try:
            response = requests.get(f"{self.host}/get_user?user_id={user_id}").json()
            if response["status"] != 200:
                return None

            return User(**response["body"]["user"])
        except:
            return None
