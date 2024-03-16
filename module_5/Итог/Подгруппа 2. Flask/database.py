import sys
import traceback

import apsw

from models import GameStatus, User, GameUser, Game, Move, Rating


class Database:
    def __init__(self):
        self.database = apsw.Connection('sqlite.db')

    def close(self):
        self.database.close()

    def get_user(self, user_id: str | None, tg_id: int | None):
        try:
            query = 'SELECT * FROM users WHERE '
            if user_id is not None:
                query += 'id = ?'
                args = (user_id, )
            elif tg_id is not None:
                query += 'tg_id = ?'
                args = (tg_id, )
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

    def create_user(self, user_id: str, tg_id: int, username: str) -> User | None:
        try:
            cursor = self.database.cursor()
            cursor.execute('INSERT INTO users VALUES (?, ?, ?) RETURNING *', (user_id, tg_id, username))
            user = cursor.fetchone()
            return User(*user)
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

    def create_game(self):
        try:
            cursor = self.database.cursor()
            cursor.execute('INSERT INTO games (status) VALUES (?) RETURNING *', (GameStatus.NEW.value, ))
            game = cursor.fetchone()
            return Game(*game)
        except Exception:
            print(traceback.format_exc(), file=sys.stderr)
            return None

    def add_user_to_game(self, game_id: int, user_id: str, sign: str):
        try:
            cursor = self.database.cursor()
            cursor.execute('INSERT INTO game_user (game_id, user_id, sign) VALUES (?, ?, ?)', (game_id, user_id, sign))
            user = self.get_user(user_id, None)
            return GameUser(user.user_id, user.username, sign)
        except Exception:
            print(traceback.format_exc(), file=sys.stderr)
            return None

    def remove_user_from_game(self, game_id: int, user_id: str):
        try:
            cursor = self.database.cursor()
            cursor.execute('DELETE FROM game_user WHERE game_id = ? AND user_id = ?', (game_id, user_id))
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

    def get_game_users(self, game_id: int) -> list[GameUser] | None:
        try:
            cursor = self.database.cursor()
            query = "SELECT users.id, users.username, game_user.sign FROM users " \
                    "JOIN game_user ON game_user.user_id = users.id " \
                    "WHERE game_user.game_id = ?"
            args = (game_id, )
            cursor.execute(query, args)
            rows = cursor.fetchall()
            users = [GameUser(*x) for x in rows]
            return users
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

    def get_moves(self, game_id: int) -> list[Move] | None:
        try:
            cursor = self.database.cursor()
            cursor.execute('SELECT * FROM moves WHERE game_id = ? ORDER BY created_at', (game_id, ))
            rows = cursor.fetchall()
            moves = [Move(*x) for x in rows]
            return moves
        except Exception:
            print(traceback.format_exc(), file=sys.stderr)
            return None

    def create_move(self, game_id: int, user_id: str, col: int, row: int, sign: str):
        try:
            cursor = self.database.cursor()
            cursor.execute('INSERT INTO moves (game_id, user_id, col, row, sign) VALUES (?, ?, ?, ?, ?) RETURNING *', (game_id, user_id, col, row, sign))
            move = cursor.fetchone()
            return Move(*move)
        except Exception:
            print(traceback.format_exc(), file=sys.stderr)
            return None

    def create_win(self, game_id: int, user_id: str):
        try:
            cursor = self.database.cursor()
            cursor.execute('INSERT INTO wins (game_id, user_id) VALUES (?, ?) RETURNING *', (game_id, user_id))
            win = cursor.fetchone()
            return win
        except Exception:
            print(traceback.format_exc(), file=sys.stderr)
            return None

    def get_rating(self) -> list[Rating] | None:
        try:
            cursor = self.database.cursor()
            cursor.execute('SELECT users.username, COUNT(wins.user_id) FROM users JOIN wins ON wins.user_id = users.id GROUP BY users.username ORDER BY COUNT(wins.user_id) DESC')
            rows = cursor.fetchall()
            rating = [Rating(*x) for x in rows]
            return rating
        except Exception:
            print(traceback.format_exc(), file=sys.stderr)
            return None
