# Внимание! Код в хранилище может отличаться от кода в репозитории.
# Код в репозитории обновляется гораздо быстрее, чем код в хранилище,
# если вдруг вносятся какие-то фиксы багов.
# Ссылка на репозиторий: https://github.com/Norrica/NewPythonCourse

import json
import uuid

from flask import Flask, request
from database import Database
from models import GameStatus

app = Flask(__name__)


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


class Response:
    def __init__(self, status, body):
        self.status = status
        self.body = body

    def json(self):
        return json.dumps(self, default=lambda o: o.__dict__)


@app.route('/')
def index():
    return 'Hello world!'


@app.route('/get_user')
def get_user():
    user_id = request.args.get('user_id', None, str)
    tg_id = request.args.get('tg_id', None, int)
    if user_id is None and tg_id is None:
        return Response(400, {"error": 'user_id or tg_id is required'}).json()

    db = Database()
    user = db.get_user(user_id, tg_id)
    db.close()
    if user is None:
        return Response(404, {"error": 'user not found'}).json()

    return Response(200, {"user": user.__dict__}).json()


@app.route('/create_user')
def create_user():
    tg_id = request.args.get('tg_id', None, int)
    username = request.args.get('username', None, str)

    if tg_id is None:
        return Response(400, {"error": 'tg_id is required'}).json()
    if username is None:
        return Response(400, {"error": 'username is required'}).json()

    user_id = str(uuid.uuid4())

    db = Database()
    user = db.create_user(user_id, tg_id, username)
    db.close()

    if user is None:
        return Response(500, {"error": 'error while adding user'}).json()

    return Response(200, {"user": user.__dict__}).json()


@app.route('/join_game')
def join_game():
    user_id = request.args.get('user_id', None, str)
    if user_id is None:
        return Response(400, {"error": 'user_id is required'}).json()

    db = Database()

    already_joined_game = db.get_game_by_user_id_and_status(user_id, GameStatus.ACTIVE)
    if already_joined_game is not None:
        game_users = db.get_game_users(already_joined_game.game_id)
        db.close()
        return Response(200, {
            "game": already_joined_game.__dict__,
            "users": [x.__dict__ for x in game_users],
        }).json()

    game = db.get_game_by_status(GameStatus.NEW)
    if game is not None:
        game_users = db.get_game_users(game.game_id)
        sign = '0' if len(game_users) == 1 else 'X'

        game_user = db.add_user_to_game(game.game_id, user_id, sign)
        if game_user is None:
            db.close()
            return Response(500, {"error": 'error while adding user to game'}).json()

        game_users.append(game_user)
        if len(game_users) == 2:
            game = db.update_game_status(game.game_id, GameStatus.ACTIVE)
            if game is None:
                db.close()
                return Response(500, {"error": 'error while starting game'}).json()
        db.close()
        return Response(200, {
            "game": game.__dict__,
            "users": [x.__dict__ for x in game_users],
        }).json()

    game = db.create_game()
    if game is None:
        db.close()
        return Response(500, {"error": 'error while creating game'}).json()

    game_user = db.add_user_to_game(game.game_id, user_id, 'X')
    if game_user is None:
        db.close()
        return Response(500, {"error": 'error while adding user to game'}).json()

    db.close()
    return Response(200, {
        "game": game.__dict__,
        "users": [game_user.__dict__],
    }).json()


@app.route('/leave_game')
def leave_game():
    user_id = request.args.get('user_id', None, str)
    game_id = request.args.get('game_id', None, int)
    if user_id is None:
        return Response(400, {"error": 'user_id is required'}).json()
    if game_id is None:
        return Response(400, {"error": 'game_id is required'}).json()

    db = Database()

    game = db.get_game_by_id(game_id)
    if game is None:
        db.close()
        return Response(404, {"error": 'game not found'}).json()

    game_users = db.get_game_users(game_id)
    if len(game_users) == 1:
        db.update_game_status(game_id, GameStatus.NEW)
    elif len(game_users) == 2:
        db.update_game_status(game_id, GameStatus.FINISHED)
        winner = [x for x in game_users if x.user_id != user_id][0]
        db.create_win(game_id, winner.user_id)
        db.update_game_winner(game_id, winner.user_id)

    db.remove_user_from_game(game_id, user_id)

    db.close()
    return Response(200, {"removed": "ok"}).json()


@app.route('/get_active_game_by_user_id')
def get_game():
    user_id = request.args.get('user_id', None, str)
    if user_id is None:
        return Response(400, {"error": 'user_id is required'}).json()

    db = Database()
    game = db.get_game_by_user_id_and_status(user_id, GameStatus.ACTIVE)

    if game is None:
        return Response(404, {"error": 'game not found'}).json()

    game_users = db.get_game_users(game.game_id)
    moves = db.get_moves(game.game_id)
    db.close()

    return Response(200, {
        "game": game.__dict__,
        "users": [x.__dict__ for x in game_users],
        "moves": [x.__dict__ for x in moves],
    }).json()


@app.route('/get_game_info')
def get_game_info():
    game_id = request.args.get('game_id', None, type=int)
    if game_id is None:
        return Response(400, {"error": 'game_id is required'}).json()

    db = Database()
    game_users = db.get_game_users(game_id)
    game = db.get_game_by_id(game_id)
    moves = db.get_moves(game_id)
    db.close()

    if game is None:
        return Response(404, {"error": 'game not found'}).json()

    return Response(200, {
        "game": game.__dict__,
        "users": [x.__dict__ for x in game_users],
        "moves": [x.__dict__ for x in moves],
    }).json()


@app.route('/make_move')
def make_move():
    game_id = request.args.get('game_id', None, type=int)
    user_id = request.args.get('user_id', None, str)
    row = request.args.get('row', None, type=int)
    col = request.args.get('col', None, type=int)
    sign = request.args.get('sign', None, str)
    if game_id is None:
        return Response(400, {"error": 'game_id is required'}).json()
    if user_id is None:
        return Response(400, {"error": 'user_id is required'}).json()
    if row is None:
        return Response(400, {"error": 'row is required'}).json()
    if col is None:
        return Response(400, {"error": 'col is required'}).json()
    if sign is None:
        return Response(400, {"error": 'sign is required'}).json()

    db = Database()
    game = db.get_game_by_id(game_id)
    if game is None:
        db.close()
        return Response(404, {"error": 'game not found'}).json()

    moves = db.get_moves(game_id)
    count_x = len([x for x in moves if x.sign == 'X'])
    count_0 = len([x for x in moves if x.sign == '0'])
    if sign == 'X' and count_x > count_0:
        db.close()
        return Response(400, {"error": 'not your turn'}).json()
    if sign == '0' and count_0 >= count_x:
        db.close()
        return Response(400, {"error": 'not your turn'}).json()

    move = db.create_move(game_id, user_id, col, row, sign)
    if move is None:
        db.close()
        return Response(500, {"error": 'error while making move'}).json()

    moves = db.get_moves(game_id)
    board = [[None for _ in range(3)] for _ in range(3)]
    for move in moves:
        board[move.row][move.col] = move.sign

    winner_sign = check_winner(board)
    if winner_sign is not None:
        game = db.update_game_status(game_id, GameStatus.FINISHED)
        if game is None:
            db.close()
            return Response(500, {"error": 'error while finishing game'}).json()
        users = db.get_game_users(game_id)
        winner = [x for x in users if x.sign == winner_sign][0]
        db.create_win(game_id, winner.user_id)
        db.update_game_winner(game_id, winner.user_id)

    if len(moves) == 9:
        game = db.update_game_status(game_id, GameStatus.FINISHED)
        if game is None:
            db.close()
            return Response(500, {"error": 'error while finishing game'}).json()

    db.close()
    return Response(200, {"move": move.__dict__}).json()


@app.route('/get_rating')
def get_rating():
    db = Database()
    rating = db.get_rating()
    if rating is None:
        db.close()
        return Response(500, {"error": 'error while getting rating'}).json()
    db.close()
    return Response(200, {"rating": [x.__dict__ for x in rating]}).json()


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=80)
