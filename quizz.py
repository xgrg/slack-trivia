import os
import os.path as op
token = os.environ['TOKEN']

import pickle
from collections import OrderedDict
import slack
from bot import *

class Trivia():
    pending_question = None
    replies = []
    scores = OrderedDict()
    previous = None

    def __init__(self, client):
        self.client = client

    def post(self, payload, channel):
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
        backup = [self.pending_question, self.replies, self.table]
        pickle.dump(backup, open('/tmp/trivia.dump', 'wb'))

    def load(self):
        fp = '/tmp/trivia.dump'
        if op.isfile(fp):
            backup = pickle.load(open(fp, 'rb'))
            pending_question, replies, table = backup
            self.pending_question = pending_question
            self.replies = replies




@slack.RTMClient.run_on(event='message')
def on_message(**payload):
    print('ON_MESSAGE')
    print(trivia.pending_question)
    data = payload['data']

    if 'text' not in data:
        print('text not in data')
        return

    text = data['text'].strip(' ')
    if not trivia.pending_question is None:
        print('PENDING QUESTION DETECTED')
        if text.lower() in ['a', 'b', 'c', 'd', 'e', 'f']:
            on_reply(payload, trivia)

        elif text.startswith('!next'):
            on_next(payload, trivia)

        elif text == '!':
            on_ping(payload, trivia)

    else:
        print('NO PENDING QUESTION')
        if text.startswith('!quizz'):
            on_quizz(payload, trivia)

    if text.startswith('!create'):
        on_create(payload, trivia)
        on_json(payload, trivia)

    elif text.startswith('!json'):
        on_json(payload, trivia)

    else:
        print('ELSE')
        #print(payload)


client = slack.RTMClient(token=token, auto_reconnect=True)
trivia = Trivia(client)
trivia.load()
trivia.client.start()
