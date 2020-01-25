import unittest
from trivia import payload as pl
import json, string
import os
import slack
from trivia.trivia import Trivia
from trivia import bot, functions

token = os.environ['TOKEN']
questions_fp = 'data/questions.json'
su = ['goperto']

class RunThemAll(unittest.TestCase):

    def setUp(self):
        self.trivia = Trivia(token, questions_fp, su)
        client = slack.WebClient(token=token)
        self.trivia.table = functions.get_users_table(client)


    def test_001(self):
        scores = {}
        replies = []
        questions = json.loads(''.join(open(questions_fp).read().split('\n')))

        for question in questions:
            text, options, correct, author = question
            if str(correct).isdigit():
                correct = string.ascii_uppercase[correct]
            else:
                correct = correct.upper()
            question = text, options, correct, author
            pl.create_question(text, options, author)

            pl.create_reply(text, options, correct, 'A', author)
            pl.solve_question(question, replies)

        pl.display_scores(scores, replies)


    def test_002(self):

        question = ('Which of these does not refer to hippocampal anatomy?', ['dentate gyrus', 'parasubiculum', 'BA36', 'CA2'], 'C', 'goperto')
        text, options, correct, author = question
        self.trivia.pending_question = question

        payload = {'rtm_client': None,
            'web_client': None, 'data': {'client_msg_id': '005b8973-7a19-490c-9fe8-73bae7edf7bf', 'suppress_notification': False, 'text': '!', 'user': 'U3RBQ239C',
            'team': 'T3Q0CB4SU', 'blocks': [{'type': 'rich_text', 'block_id': 'y3oZZ', 'elements': [{'type': 'rich_text_section', 'elements': [{'type': 'text', 'text': '!'}]}]}],
            'user_team': 'T3Q0CB4SU', 'source_team': 'T3Q0CB4SU', 'channel': 'DRZFMPSKA', 'event_ts': '1579968359.012800', 'ts': '1579968359.012800'}}
        bot.on_ping(payload, self.trivia)
        bot.on_scores(payload, self.trivia)
        payload['data']['text'] = '!quizz'
        bot.on_message(payload, self.trivia)
        payload['data']['text'] = '!'
        bot.on_message(payload, self.trivia)
        payload['data']['text'] = 'z'
        bot.on_message(payload, self.trivia)
        payload['data']['text'] = 'a'
        bot.on_message(payload, self.trivia)
        payload['data']['text'] = 'b'
        bot.on_message(payload, self.trivia)
        payload['data']['text'] = '!'
        bot.on_message(payload, self.trivia)
        reply = ('quizzbot', True, 'A')
        self.trivia.replies.append(reply)
        payload['data']['text'] = '!next'
        bot.on_message(payload, self.trivia)
        payload['data']['text'] = '!quizz'
        bot.on_message(payload, self.trivia)

        payload['data']['text'] = 'test'
        bot.on_message(payload, self.trivia)
        payload['data']['text'] = '!create toto [a,b,c,d] 1'
        bot.on_message(payload, self.trivia)
        payload['data']['text'] = '!create toto [a,b,c,d] b'
        bot.on_message(payload, self.trivia)
        payload['data']['text'] = '!create toto [a,b,c,d] bqs'
        bot.on_message(payload, self.trivia)
        payload['data']['text'] = '!scores'
        bot.on_message(payload, self.trivia)
        payload['data']['text'] = '!scores_reset'
        bot.on_message(payload, self.trivia)
        payload['data']['text'] = '!json'
        bot.on_message(payload, self.trivia)



    def test_003(self):
        client = slack.WebClient(token=token)
        #functions.get_users_table(client)
        functions.get_channel_id(client, 'general')
