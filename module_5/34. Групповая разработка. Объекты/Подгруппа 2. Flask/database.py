import sys
import traceback

import apsw

from models import User, Game, GameStatus, GameUser


class Database:
    def __init__(self):
        self.database = apsw.Connection('sqlite.db')

    def close(self):
        self.database.close()

    def create_user(self, user_id: str, tg_id: int, username: str) -> User | None:
        try:
            cursor = self.database.cursor()
            cursor.execute('INSERT INTO users VALUES (?, ?, ?) RETURNING *', (user_id, tg_id, username))
            user = cursor.fetchone()
            return User(*user)
        except Exception:
            print(traceback.format_exc(), file=sys.stderr)
            return None

    def get_user(self, user_id: str | None, tg_id: int | None):
        try:
            query = 'SELECT * FROM users WHERE '
            if user_id is not None:
                query += 'id = ?'
                args = (user_id,)
            elif tg_id is not None:
                query += 'tg_id = ?'
                args = (tg_id,)
            else:
                return None
            cursor = self.database.cursor()
            cursor.execute(query, args)
            user = cursor.fetchone()
            if user is None:
                return None
            return User(*user)
        except Exception:
            print(traceback.format_exc(), file=sys.stderr)
            return None

    def create_game(self):
        try:
            cursor = self.database.cursor()
            cursor.execute('INSERT INTO games (status) VALUES (?) RETURNING *', (GameStatus.NEW.value, ))
            game = cursor.fetchone()
            return Game(*game)
        except Exception:
            print(traceback.format_exc(), file=sys.stderr)
            return None

    def get_game_by_id(self, game_id: int) -> Game | None:
        try:
            cursor = self.database.cursor()
            cursor.execute('SELECT * FROM games WHERE id = ?', (game_id, ))
            game = cursor.fetchone()
            if game is None:
                return None
            return Game(*game)
        except Exception:
            print(traceback.format_exc(), file=sys.stderr)
            return None

    def get_game_by_status(self, status: GameStatus) -> Game | None:
        try:
            cursor = self.database.cursor()
            cursor.execute('SELECT * FROM games WHERE status = ?', (status.value, ))
            game = cursor.fetchone()
            if game is None:
                return None
            return Game(*game)
        except Exception:
            print(traceback.format_exc(), file=sys.stderr)
            return None

    def update_game_status(self, game_id: int, status: GameStatus) -> Game | None:
        try:
            cursor = self.database.cursor()
            cursor.execute("UPDATE games SET status = ? WHERE id = ? RETURNING *", (status.value, game_id))
            game = cursor.fetchone()
            return Game(*game)
        except Exception:
            print(traceback.format_exc(), file=sys.stderr)
            return None

    def update_game_winner(self, game_id: int, winner_id: str) -> Game | None:
        try:
            cursor = self.database.cursor()
            cursor.execute("UPDATE games SET winner_id = ? WHERE id = ? RETURNING *", (winner_id, game_id))
            game = cursor.fetchone()
            return Game(*game)
        except Exception:
            print(traceback.format_exc(), file=sys.stderr)
            return None

    def add_user_to_game(self, game_id: int, user_id: str, sign: str):
        try:
            query = 'INSERT INTO game_user (game_id, user_id, sign) VALUES (?, ?, ?)'
            args = (game_id, user_id, sign)
            cursor = self.database.cursor()
            cursor.execute(query, args)
            user = self.get_user(user_id, None)
            return GameUser(user.user_id, user.username, sign)
        except Exception:
            print(traceback.format_exc(), file=sys.stderr)
            return None

    def remove_user_from_game(self, game_id: int, user_id: str):
        try:
            query = 'DELETE FROM game_user WHERE game_id = ? AND user_id = ?'
            args = (game_id, user_id)
            cursor = self.database.cursor()
            cursor.execute(query, args)
        except Exception:
            print(traceback.format_exc(), file=sys.stderr)
            return None

    def get_game_by_user_id_and_status(self, user_id: str, status: GameStatus) -> Game | None:
        try:
            query = "SELECT games.* FROM games " \
                    "JOIN game_user ON game_user.game_id = games.id " \
                    "WHERE game_user.user_id = ? AND games.status = ?"
            args = (user_id, status.value)
            cursor = self.database.cursor()
            cursor.execute(query, args)
            game = cursor.fetchone()
            if game is None:
                return None
            return Game(*game)
        except Exception:
            print(traceback.format_exc(), file=sys.stderr)

    def get_game_users(self, game_id: int) -> list[GameUser] | None:
        try:
            cursor = self.database.cursor()
            query = "SELECT users.id, users.username, game_user.sign FROM users " \
                    "JOIN game_user ON game_user.user_id = users.id " \
                    "WHERE game_user.game_id = ?"
            args = (game_id, )
            cursor.execute(query, args)
            rows = cursor.fetchall()
            users = [GameUser(*user) for user in rows]
            return users
        except Exception:
            print(traceback.format_exc(), file=sys.stderr)
            return None

    def create_win(self, game_id: int, user_id: str):
        try:
            query = 'INSERT INTO wins (game_id, user_id) VALUES (?, ?)'
            args = (game_id, user_id)
            cursor = self.database.cursor()
            cursor.execute(query, args)
            win = cursor.fetchone()
            return win
        except Exception:
            print(traceback.format_exc(), file=sys.stderr)
            return None
