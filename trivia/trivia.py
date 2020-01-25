
import pickle
import os.path as op

class Trivia():
    pending_question = None
    replies = []
    scores = {}
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
