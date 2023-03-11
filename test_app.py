from unittest import TestCase

from flask import jsonify

from app import app, games
from boggle import BoggleGame

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client as client:
            response = client.get('/')
            html = response.get_data(as_text=True)

            # test that you're getting a template
            self.assertEqual(response.status_code, 200)
            self.assertIn('<!-- Test: homepage -->', html)

    def test_api_new_game(self):
        """Test starting a new game."""

        with self.client as client:

            # write a test for this route
            response = client.post("/api/new-game")

            json_data = response.get_json()

            response_id = json_data["gameId"]
            response_board = json_data["board"]

            #test that sent id is in games
            self.assertTrue(games[response_id])

            #test that the game board at that id is equal to the response board
            self.assertEqual(games[response_id].board, response_board)

    def test_api_score_word(self):
        """Test scoring a word and returning a JSON"""

        with self.client as client:

            g = BoggleGame()
            g.board = [
                ['X','X','X','X','X'],
                ['X','X','C','X','X'],
                ['X','X','A','X','X'],
                ['X','X','T','X','X'],
                ['X','X','X','X','X']
                ]
            games['id'] = g
            data = {'gameId': 'id', 'word': 'XKJDF'}

            response = client.post("/api/score-word",
                                   jsonify(data))
            json_data = response.get_json()
            self.assertEqual(json_data, '{"result": "not-word"}')


