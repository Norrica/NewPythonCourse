import aiohttp

from models import User, Rating


class HttpClient:
    def __init__(self):
        self.session = aiohttp.ClientSession()
        self.host = "https://tictac.redko.us"
        self.cache = {}

    async def get_user(self, tg_id: int) -> User | None:
        if tg_id in self.cache:
            return self.cache[tg_id]
        async with self.session.get(f"{self.host}/get_user?tg_id={tg_id}") as response:
            if response.status == 200:
                data = await response.json(content_type=None)
                if data["status"] == 200:
                    user = User(**data["body"]["user"])
                    self.cache[tg_id] = user
                    return user
            return None

    async def create_user(self, tg_id: int, username: str) -> User | None:
        url = f"{self.host}/create_user?tg_id={tg_id}&username={username}"
        async with self.session.get(url) as response:
            if response.status == 200:
                data = await response.json(content_type=None)
                if data["status"] == 200:
                    user = User(**data["body"]["user"])
                    self.cache[tg_id] = user
                    return user
            return None

    async def get_rating(self) -> list[Rating] | None:
        async with self.session.get(f"{self.host}/get_rating") as response:
            if response.status == 200:
                data = await response.json(content_type=None)
                if data["status"] == 200:
                    return [Rating(**rating) for rating in data["body"]["rating"]]

            return None

    async def close_session(self):
        await self.session.close()
