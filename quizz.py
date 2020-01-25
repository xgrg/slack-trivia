import os
import slack

token = os.environ['TOKEN']
questions_fp = 'data/questions.json'
su = ['goperto', 'quizzbot'] # superuser

from trivia.trivia import Trivia
from trivia import bot

@slack.RTMClient.run_on(event='message')
def on_message(**payload):
    bot.on_message(payload, trivia)

if __name__ == '__main__':
    trivia = Trivia(token, questions_fp, su)
    trivia.client.start()
