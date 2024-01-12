import datetime
import sqlite3
import json
import traceback
import uuid
from enum import Enum

from flask import Flask, request


# GAME STATUSES
class GameStatus(Enum):
    NEW = 0
    ACTIVE = 1
    FINISHED = 2


def check_winner(board):
    # Проверка горизонтальных и вертикальных комбинаций
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] is not None:
            return board[i][0]  # Горизонтальная победа
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] is not None:
            return board[0][i]  # Вертикальная победа

    # Проверка диагональных комбинаций
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]  # Главная диагональ
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]  # Побочная диагональ

    # Если ни один из игроков не выиграл
    return None

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


class Database:
    def __init__(self):
        self.database = sqlite3.connect('sqlite.db')
        self.cursor = self.database.cursor()

    def close(self):
        self.database.close()

    def get_user(self, user_id: str | None, tg_id: int | None):
        try:
            if user_id is not None:
                query = 'SELECT * FROM users WHERE id = ?'
                args = (user_id, )
            else:
                query = 'SELECT * FROM users WHERE tg_id = ?'
                args = (tg_id, )
            cursor = self.database.cursor()
            cursor.execute(query, args)
            user = cursor.fetchone()
            if user is None:
                return None
            return User(user[0], user[1], user[2])
        except Exception as e:
            print(traceback.format_exc())
            return None

    def create_user(self, user_id: str, tg_id: int, username: str) -> User | None:
        try:
            cursor = self.database.cursor()
            cursor.execute('INSERT INTO users VALUES (?, ?, ?) RETURNING *', (user_id, tg_id, username))
            user = cursor.fetchone()
            self.database.commit()
            return User(user[0], user[1], user[2])
        except Exception as e:
            print(traceback.format_exc())
            return None

    def get_game_by_status(self, status: GameStatus) -> Game | None:
        try:
            cursor = self.database.cursor()
            cursor.execute('SELECT * FROM games WHERE status = ?', (status.value, ))
            game = cursor.fetchone()
            if game is None:
                return None
            return Game(game[0], game[1], game[2])
        except Exception as e:
            print(traceback.format_exc())
            return None

    def get_game_by_user_id_and_status(self, user_id: str, status: GameStatus) -> Game | None:
        query = "SELECT games.* from games " \
                "JOIN game_user ON game_user.game_id = games.id " \
                "WHERE game_user.user_id = ? AND games.status = ?"
        args = (user_id, status.value)
        cursor = self.database.cursor()
        cursor.execute(query, args)
        game = cursor.fetchone()
        if game is None:
            return None
        return Game(game[0], game[1], game[2])

    def create_game(self):
        try:
            cursor = self.database.cursor()
            cursor.execute('INSERT INTO games (status) VALUES (?) RETURNING *', (GameStatus.NEW.value, ))
            game = cursor.fetchone()
            self.database.commit()
            return Game(game[0], game[1], game[2])
        except Exception as e:
            print(traceback.format_exc())
            return None

    def add_user_to_game(self, game_id: int, user_id: str, sign: str):
        try:
            cursor = self.database.cursor()
            cursor.execute('INSERT INTO game_user (game_id, user_id, sign) VALUES (?, ?, ?)', (game_id, user_id, sign))
            user = self.get_user(user_id, None)
            self.database.commit()
            return GameUser(user.user_id, user.username, sign)
        except Exception as e:
            print(traceback.format_exc())
            return None

    def update_game(self, game_id: int, status: GameStatus) -> Game | None:
        try:
            cursor = self.database.cursor()
            cursor.execute("UPDATE games SET status = ? WHERE id = ? RETURNING *", (status.value, game_id))
            game = cursor.fetchone()
            self.database.commit()
            return Game(game[0], game[1], game[2])
        except Exception as e:
            print(traceback.format_exc())
            return None

    def get_game_users(self, game_id: int) -> list[GameUser] | None:
        try:
            cursor = self.database.cursor()
            query = "SELECT users.id, users.username, game_user.sign FROM users JOIN game_user ON game_user.user_id = users.id WHERE game_user.game_id = ?"
            args = (game_id, )
            cursor.execute(query, args)
            rows = cursor.fetchall()
            users = [GameUser(x[0], x[1], x[2]) for x in rows]
            return users
        except Exception as e:
            print(traceback.format_exc())
            return None

    def get_game_by_id(self, game_id: int) -> Game | None:
        try:
            cursor = self.database.cursor()
            cursor.execute('SELECT * FROM games WHERE id = ?', (game_id, ))
            game = cursor.fetchone()
            if game is None:
                return None
            return Game(game[0], game[1], game[2])
        except Exception as e:
            print(traceback.format_exc())
            return None

    def get_moves(self, game_id: int) -> list[Move] | None:
        try:
            cursor = self.database.cursor()
            cursor.execute('SELECT * FROM moves WHERE game_id = ? ORDER BY created_at', (game_id, ))
            rows = cursor.fetchall()
            moves = [Move(x[0], x[1], x[2], x[3], x[4], x[5], x[6]) for x in rows]
            return moves
        except Exception as e:
            print(traceback.format_exc())
            return None

    def create_move(self, game_id: int, user_id: str, col: int, row: int, sign: str):
        try:
            cursor = self.database.cursor()
            cursor.execute('INSERT INTO moves (game_id, user_id, col, row, sign) VALUES (?, ?, ?, ?, ?) RETURNING *', (game_id, user_id, col, row, sign))
            move = cursor.fetchone()
            self.database.commit()
            return Move(move[0], move[1], move[2], move[3], move[4], move[5], move[6])
        except Exception as e:
            print(traceback.format_exc())
            return None

    def create_win(self, game_id: int, user_id: str):
        try:
            cursor = self.database.cursor()
            cursor.execute('INSERT INTO wins (game_id, user_id) VALUES (?, ?) RETURNING *', (game_id, user_id))
            win = cursor.fetchone()
            self.database.commit()
            return win
        except Exception as e:
            print(traceback.format_exc())
            return None

    def get_rating(self):
        try:
            cursor = self.database.cursor()
            cursor.execute('SELECT users.username, COUNT(wins.user_id) FROM users JOIN wins ON wins.user_id = users.id GROUP BY users.username ORDER BY COUNT(wins.user_id) DESC')
            rows = cursor.fetchall()
            rating = [Rating(x[0], x[1]) for x in rows]
            return rating
        except Exception as e:
            print(traceback.format_exc())
            return None


class Response:
    def __init__(self, status, body):
        self.status = status
        self.body = body

    def json(self):
        return json.dumps(self, default=lambda o: o.__dict__)


app = Flask(__name__)


@app.route('/get_user')
def get_user():
    user_id = request.args.get('user_id', None, str)
    tg_id = request.args.get('tg_id', None, int)
    if user_id is None and tg_id is None:
        return Response(400, 'user_id or tg_id is required').json()

    db = Database()
    user = db.get_user(user_id, tg_id)
    db.close()
    if user is None:
        return Response(404, 'user not found').json()

    return Response(200, {"user": user.__dict__}).json()


@app.route('/create_user')
def create_user():
    user_id = request.args.get('user_id', None, str)
    tg_id = request.args.get('tg_id', None, int)
    username = request.args.get('username', None, str)

    if user_id is None:
        return Response(400, 'user_id is required').json()
    if tg_id is None:
        return Response(400, 'tg_id is required').json()
    if username is None:
        return Response(400, 'username is required').json()

    db = Database()
    user = db.create_user(user_id, tg_id, username)
    db.close()

    if user is None:
        return Response(500, 'error while adding user').json()

    return Response(200, {"user": user.__dict__}).json()


@app.route('/get_active_game_by_user_id')
def get_game():
    user_id = request.args.get('user_id', None, str)
    if user_id is None:
        return Response(400, 'user_id is required').json()

    db = Database()
    game = db.get_game_by_user_id_and_status(user_id, GameStatus.ACTIVE)

    if game is None:
        return Response(404, 'game not found').json()

    game_users = db.get_game_users(game.game_id)
    moves = db.get_moves(game.game_id)
    db.close()

    return Response(200, {"game": game.__dict__, "users": [x.__dict__ for x in game_users], "moves": [x.__dict__ for x in moves]}).json()


@app.route('/join_game')
def join_game():
    user_id = request.args.get('user_id', None, str)
    if user_id is None:
        return Response(400, 'user_id is required').json()

    db = Database()

    already_joined_game = db.get_game_by_user_id_and_status(user_id, GameStatus.ACTIVE)
    if already_joined_game is not None:
        game_users = db.get_game_users(already_joined_game.game_id)
        db.close()
        return Response(200, {"game": already_joined_game.__dict__, "users": [x.__dict__ for x in game_users]}).json()

    already_waiting_game = db.get_game_by_user_id_and_status(user_id, GameStatus.NEW)
    if already_waiting_game is not None:
        game_users = db.get_game_users(already_waiting_game.game_id)
        db.close()
        return Response(200, {"game": already_waiting_game.__dict__, "users": [x.__dict__ for x in game_users]}).json()

    game = db.get_game_by_status(GameStatus.NEW)
    if game is not None:
        game_user = db.add_user_to_game(game.game_id, user_id, '0')
        if game_user is None:
            db.close()
            return Response(500, 'error while adding user to game').json()

        game_users = db.get_game_users(game.game_id)
        game = db.update_game(game.game_id, GameStatus.ACTIVE)
        if game is None:
            db.close()
            return Response(500, 'error while starting game').json()
        db.close()
        return Response(200, {"game": game.__dict__, "users": [x.__dict__ for x in game_users]}).json()

    game = db.create_game()
    if game is None:
        db.close()
        return Response(500, 'error while creating game').json()

    game_user = db.add_user_to_game(game.game_id, user_id, 'X')
    if game_user is None:
        db.close()
        return Response(500, 'error while adding user to game').json()

    db.close()
    return Response(200, {"game": game.__dict__, "users": [game_user.__dict__]}).json()


@app.route('/get_game_info')
def get_game_info():
    game_id = request.args.get('game_id', None, type=int)
    if game_id is None:
        return Response(400, 'game_id is required').json()

    db = Database()
    game_users = db.get_game_users(game_id)
    game = db.get_game_by_id(game_id)
    moves = db.get_moves(game_id)
    db.close()

    if game is None:
        return Response(404, 'game not found').json()

    return Response(200, {"game": game.__dict__, "users": [x.__dict__ for x in game_users], "moves": [x.__dict__ for x in moves]}).json()


@app.route('/make_move')
def make_move():
    game_id = request.args.get('game_id', None, type=int)
    user_id = request.args.get('user_id', None, str)
    row = request.args.get('row', None, type=int)
    col = request.args.get('col', None, type=int)
    sign = request.args.get('sign', None, str)
    if game_id is None:
        return Response(400, 'game_id is required').json()
    if user_id is None:
        return Response(400, 'user_id is required').json()
    if row is None:
        return Response(400, 'row is required').json()
    if col is None:
        return Response(400, 'col is required').json()
    if sign is None:
        return Response(400, 'sign is required').json()

    db = Database()
    game = db.get_game_by_id(game_id)
    if game is None:
        db.close()
        return Response(404, 'game not found').json()

    move = db.create_move(game_id, user_id, col, row, sign)
    if move is None:
        db.close()
        return Response(500, 'error while making move').json()

    moves = db.get_moves(game_id)
    board = [[None for _ in range(3)] for _ in range(3)]
    for move in moves:
        board[move.row][move.col] = move.sign

    winner_sign = check_winner(board)
    if winner_sign is not None:
        game = db.update_game(game_id, GameStatus.FINISHED)
        if game is None:
            db.close()
            return Response(500, 'error while finishing game').json()
        users = db.get_game_users(game_id)
        winner = [x for x in users if x.sign == winner_sign][0]
        db.create_win(game_id, winner.user_id)

    if len(moves) == 9:
        game = db.update_game(game_id, GameStatus.FINISHED)
        if game is None:
            db.close()
            return Response(500, 'error while finishing game').json()

    db.close()
    return Response(200, {"move": move.__dict__}).json()


@app.route('/get_rating')
def get_rating():
    db = Database()
    rating = db.get_rating()
    if rating is None:
        db.close()
        return Response(500, 'error while getting rating').json()
    db.close()
    return Response(200, {"rating": [x.__dict__ for x in rating]}).json()


@app.route('/ping')
def ping():
    return Response(200, 'pong').json()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
