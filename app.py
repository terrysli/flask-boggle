from flask import Flask, request, render_template, jsonify
from uuid import uuid4

from boggle import BoggleGame

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"

# The boggle games created, keyed by game id
games = {}
test_game = BoggleGame()
test_game.board = [
    ['X','X','X','X','X'],
    ['X','X','C','X','X'],
    ['X','X','A','X','X'],
    ['X','X','T','X','X'],
    ['X','X','X','X','X']
    ]
games['testid'] = test_game

@app.get("/")
def homepage():
    """Show board."""

    return render_template("index.html")


@app.post("/api/new-game")
def new_game():
    """Start a new game and return JSON: {game_id, board}."""

    # get a unique string id for the board we're creating
    game_id = str(uuid4())
    game = BoggleGame()
    games[game_id] = game

    return jsonify({"gameId": game_id , "board": game.board})


@app.post("/api/score-word")
def score_word():
    """Take a gameId and word and return a JSON of whether word is a valid
    word and on the board
    """
    gameId = request.json["gameId"]
    word = request.json["word"]
    game = games[gameId]

    if not game.is_word_in_word_list(word):
        return jsonify({"result": "not-word"})
    elif not game.check_word_on_board(word):
        return jsonify({"result": "not-on-board"})
    else:
        return jsonify({"result": "not ok"})


