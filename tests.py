import unittest
import payload as pl
import json
from quizz import Trivia

class RunThemAll(unittest.TestCase):

    def setUp(self):
        pass

    def test_001(self):
        scores = {}
        replies = []
        trivia = Trivia(None)
        trivia.load()
        questions = json.loads(''.join(open('questions.json').read().split('\n')))

        for question in questions:
            text, options, correct, author = question
            pl.create_question(text, options, author)
            pl.create_reply(text, options, correct, 'A', author)
            pl.solve_question(question, replies)

        pl.display_scores(scores, replies)
