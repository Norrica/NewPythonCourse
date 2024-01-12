import sqlite3


class User:
    def __init__(self, user_id: int, city: str | None = None):
        self.user_id = user_id
        self.city = city


class Database:
    def __init__(self, path: str):
        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()

    def get_user(self, user_id: int) -> User | None:
        user = self.cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        if user is None:
            return None

        return User(user_id=user_id, city=user[1])

    def create_user(self, user_id: int):
        self.cursor.execute("INSERT INTO users(id) VALUES (?)", (user_id,))
        self.connection.commit()

    def set_city(self, user_id: int, city: str):
        self.cursor.execute("UPDATE users SET city = ? WHERE id = ?", (city, user_id))
        self.connection.commit()

    def get_users_count(self) -> int:
        return self.cursor.execute("SELECT COUNT(*) FROM users").fetchone()[0]

    def close(self):
        self.connection.close()

