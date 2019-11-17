import os
token = os.environ['TOKEN']


from collections import OrderedDict
import slack
from bot import *

class Trivia():
    pending_question = None
    replies = []
    scores = OrderedDict()

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


@slack.RTMClient.run_on(event='message')
def on_message(**payload):
    print(trivia.pending_question)
    data = payload['data']

    if 'text' not in data:
        print('text not in data')
        return
    text = data['text'].strip(' ')
    if not trivia.pending_question is None and \
            text.lower() in ['a', 'b', 'c', 'd', 'e', 'f']:
        on_reply(payload, trivia)

    elif text.startswith('!next'):
        on_next(payload, trivia)

    elif text.startswith('!quizz'):
        on_quizz(payload, trivia)

    elif text.startswith('!create'):
        on_create(payload, trivia)

    elif '!' in data['text'] and not trivia.pending_question is None:
        on_ping(payload, trivia)

    else:
        print(payload)


client = slack.RTMClient(token=token)
trivia = Trivia(client)
trivia.client.start()
