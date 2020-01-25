
import pickle
import os.path as op
import os
import slack
import string


class Trivia():
    pending_question = None
    replies = []
    scores = {}
    previous = None

    def __init__(self, token):
        self.client = slack.RTMClient(token=token, auto_reconnect=True)

    def post(self, payload, channel):
        print(payload)
        print(payload['text'])
        kwargs = {'as_user':True,
                  'channel':channel,
                  'text':payload['text'],
                  'attachments':payload['attachments']}
        response = None
        if not 'CI_TEST' in os.environ:
            response = self.webclient.chat_postMessage(**kwargs)
        return response

    def post_text(self, text, channel):
        kwargs = {'as_user':True,
                  'channel':channel,
                  'text':text}
        response = None
        if not 'CI_TEST' in os.environ:
            response = self.webclient.chat_postMessage(**kwargs)
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
