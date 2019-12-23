import schedule
import time
import os
import slack
import sys
from slack.errors import SlackApiError

chan = ''
if len(sys.argv) > 1:
    chan = sys.argv[1]

token = os.environ['TOKEN']

def post(text, channel, client):
     response = client.chat_postMessage(as_user=True,
          channel=channel,
          text=text)
     return response

pending = False
channel = 'DRZFMPSKA'

client = slack.WebClient(token=token, timeout=30)

def job():
    global pending, channel, client, chan
    try:
        if pending:
            print('NEXT')
            post('!next %s'%chan, channel, client)
        else:
            print('QUIZZ')
            post('!quizz %s'%chan, channel, client)
    except SlackApiError as e:
        print(e)
        return
    pending = not pending

#schedule.every(30).seconds.do(job)
#schedule.every().day.at('10:00').do(job)
schedule.every(2).hours.do(job)
#schedule.every().minute.do(job)
#schedule.every().day.at("10:30").do(job)

while 1:
    schedule.run_pending()
    time.sleep(1)
