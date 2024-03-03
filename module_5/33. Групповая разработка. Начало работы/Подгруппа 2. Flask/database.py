import sys
import traceback

import apsw

from models import User


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