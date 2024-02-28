import sqlite3


class User:
    def __init__(self, user_id: int, city: str | None = None):
        self.user_id = user_id
        self.city = city


class Database:
    def __init__(self):
        self.connection = sqlite3.connect("sqlite.db")
        self.cursor = self.connection.cursor()

    def get_user(self, user_id: int) -> User | None:
        query = "SELECT * FROM users WHERE id = ?"
        args = (user_id,)
        self.cursor.execute(query, args)
        row = self.cursor.fetchone()
        if row is None:
            return None

        return User(user_id=user_id, city=row[1])

    def create_user(self, user_id: int):
        query = "INSERT INTO users(id) VALUES (?)"
        args = (user_id,)
        self.cursor.execute(query, args)
        self.connection.commit()

    def set_city(self, user_id: int, city: str):
        query = "UPDATE users SET city = ? WHERE id = ?"
        args = (city, user_id)
        self.cursor.execute(query, args)
        self.connection.commit()

    def get_users_count(self) -> int:
        query = "SELECT COUNT(*) FROM users"
        self.cursor.execute(query)
        row = self.cursor.fetchone()

        return row[0]

    def close(self):
        self.connection.close()

