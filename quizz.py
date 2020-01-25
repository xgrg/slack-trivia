import os
import slack
token = os.environ['TOKEN']

from trivia.trivia import Trivia
from trivia import bot


@slack.RTMClient.run_on(event='message')
def on_message(**payload):
    bot.on_message(payload, trivia)

if __name__ == '__main__':
    trivia = Trivia(token)
    trivia.load()
    trivia.client.start()
