
import os
import slack
from trivia import functions

class Trivia():
    pending_question = None
    replies = []
    scores = {}
    previous = None

    def __init__(self, token, fp, su):
        self.client = slack.RTMClient(token=token, auto_reconnect=True)
        client = slack.WebClient(token=token)
        self.table = functions.get_users_table(client)
        self.fp = fp
        self.su = su

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

    def get_user_id(self, name):
        return [k for k,v in list(self.table.items()) if v == name][0]

    def get_username(self, id):
        return self.table[id]
