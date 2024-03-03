import json
import uuid

from flask import Flask, request
from database import Database

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


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=80)
