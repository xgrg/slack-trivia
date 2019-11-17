token = ''

import slack


def get_user_id(client, name):
    response = [e for e in client.users_list().data['members']\
        if e['name'] == 'goperto']
    return response[0]['id']


def create_question(text, options):
    payload = {
        "text": text,
        "attachments": [{
                "text": "Please pick an answer.",
                "fallback": "You are unable to play",
                "callback_id": "wopr_game",
                "color": "#3AA3E3",
                "attachment_type": "default",
                "actions": [] }]
    }
    for each in options:
        option = {'name': 'game',
                  'text': each,
                  'type': 'button',
                  'value': each}
        payload['attachments'][0]['actions'].append(option)
    return payload

client = slack.WebClient(token=token, timeout=30)



client = slack.RTMClient(token=token)

@slack.RTMClient.run_on(event='message')
def say_hello(**payload):
    data = payload['data']
    if '!quizz' in data['text']:
        webclient = payload['web_client']

        payload = create_question("Would you prefer?", ['test1', 'test2', 'test3'])

        channel = get_user_id(webclient, 'goperto')

        response = webclient.chat_postMessage(as_user=True,
             channel=channel,
             text=payload['text'],
             attachments=payload['attachments'])

        channel, ts = response['channel'], response['ts']
    else:
        print(payload)

client.start()
