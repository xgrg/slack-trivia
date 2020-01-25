import os
import string
token = os.environ['TOKEN']
su = ['U3RBQ239C', 'URZFFUNL8'] # superusers (goperto and quizzbot)
from trivia import Trivia
import slack
import bot


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
            bot.on_reply(payload, trivia)

        elif text.startswith('!next') and sender in su:
            bot.on_next(payload, trivia)

        elif text == '!':
            bot.on_ping(payload, trivia)

    else:
        print('NO PENDING QUESTION')
        if text.startswith('!quizz') and sender in su:
            bot.on_quizz(payload, trivia)

    if text.startswith('!create'):
        bot.on_create(payload, trivia)
        bot.on_json(payload, trivia)

    elif text.startswith('!json') and sender in su:
        bot.on_json(payload, trivia)

    elif text == '!scores' and sender in su:
        bot.on_scores(payload, trivia)

    elif text == '!scores_reset' and sender in su:
        bot.on_scores_reset(payload, trivia)

    elif text == '!quit' and sender in su:
        import sys
        sys.exit(0)

    else:
        print('ELSE')
        #print(payload)



if __name__ == '__main__':
    client = slack.RTMClient(token=token, auto_reconnect=True)
    trivia = Trivia(client)
    trivia.load()
    trivia.client.start()
