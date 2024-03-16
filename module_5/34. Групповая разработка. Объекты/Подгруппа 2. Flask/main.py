import json
import uuid

from flask import Flask, request
from database import Database
from models import GameStatus

app = Flask(__name__)


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


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=80)
