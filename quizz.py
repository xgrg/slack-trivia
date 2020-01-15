import os
import os.path as op
token = os.environ['TOKEN']

import pickle
from collections import OrderedDict
import slack
from bot import *

su = ['U3RBQ239C', 'URZFFUNL8'] # superusers (goperto and quizzbot)

class Trivia():
    pending_question = None
    replies = []
    scores = OrderedDict()
    previous = None

    def __init__(self, client):
        self.client = client

    def post(self, payload, channel):
        print(payload)
        print(payload['text'])
        response = self.webclient.chat_postMessage(as_user=True,
             channel=channel,
             text=payload['text'],
             attachments=payload['attachments'])
        return response

    def post_text(self, text, channel):
        response = self.webclient.chat_postMessage(as_user=True,
             channel=channel,
             text=text)
        return response

    def get_params(self, payload):
        data = payload['data']
        webclient = payload['web_client']
        sender = data['user']
        self.webclient = webclient
        return data, sender

    def dump(self):
        backup = [self.pending_question, self.replies, self.table, self.scores]
        pickle.dump(backup, open('/tmp/trivia.dump', 'wb'))

    def load(self):
        fp = '/tmp/trivia.dump'
        if op.isfile(fp):
            backup = pickle.load(open(fp, 'rb'))
            pending_question, replies, table, scores = backup
            self.pending_question = pending_question
            self.replies = replies
            self.table = table
            self.scores = scores




@slack.RTMClient.run_on(event='message')
def on_message(**payload):
    print('ON_MESSAGE')
    print(trivia.pending_question)
    data = payload['data']

    if 'text' not in data:
        print('text not in data')
        return

    text = data['text'].strip(' ')
    sender = data['user']

    if not trivia.pending_question is None:
        print('PENDING QUESTION DETECTED')
        if text.upper() in string.ascii_uppercase and len(text) == 1:
            on_reply(payload, trivia)

        elif text.startswith('!next') and sender in su:
            on_next(payload, trivia)

        elif text == '!':
            on_ping(payload, trivia)

    else:
        print('NO PENDING QUESTION')
        if text.startswith('!quizz') and sender in su:
            on_quizz(payload, trivia)

    if text.startswith('!create'):
        on_create(payload, trivia)
        on_json(payload, trivia)

    elif text.startswith('!json') and sender in su:
        on_json(payload, trivia)

    elif text.startswith('!scores') and sender in su:
        on_scores(payload, trivia)

    elif text.startswith('!scores_reset') and sender in su:
        on_scores_reset(payload, trivia)

    else:
        print('ELSE')
        #print(payload)

if __name__ == '__main__':
    client = slack.RTMClient(token=token, auto_reconnect=True)
    trivia = Trivia(client)
    trivia.load()
    trivia.client.start()
