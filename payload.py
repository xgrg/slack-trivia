
def create_action_question(text, options):
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

def create_question(text, options, author):
    payload = {
        "text": 'Question: %s'%text,
        "attachments": [
            {
                "mrkdwn_in": ["text"],
                "color": "#36a64f",
                "footer": "Question by <@%s>. Reply with a letter here or in private (or type !)."%author,
                "footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png",
                "fields": []
            }
        ]
    }
    for each, letter in zip(options, 'ABCDEFGH'):
        option = {'title': '%s. %s'%(letter, each), 'short': False}
        payload['attachments'][0]['fields'].append(option)
    return payload

def create_reply(text, options, correct, reply, author):

    payload = {'text': 'The question was:',
        'attachments':

            [{"mrkdwn_in": ["text"],
            "color": "#36a64f",
            "footer": "Question by <@%s>. Reply with a letter here or in private (or type !)."%author,
            "footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png",
            "pretext": text,
            "fields": []}]
    }
    if not str(correct).isdigit():
        correct = 'ABCDEFGH'.index(correct.upper())
    for each, letter in zip(options, 'ABCDEFGH'):
        option = {'title': '%s. %s'%(letter, each), 'short': False}
        payload['attachments'][0]['fields'].append(option)
    index = 'ABCDEFGH'.index(reply)
    attch = {"mrkdwn_in": ["text"],
        "color": "#36a64f",
        "text": 'You replied: _%s. %s_'%('ABCDEFGH'[index], options[index])}
    payload['attachments'].append(attch)
    if index == correct:
        attch = {"mrkdwn_in": ["text"],
            "color": "#36a64f",
            "pretext": 'CORRECT!'}
        payload['attachments'].append(attch)
    else:
        attch = {"mrkdwn_in": ["text"],
            "color": "#36a64f",
            "text": 'The right answer was: *%s. %s*'%('ABCDEFGH'[correct], options[correct])}
        payload['attachments'].append(attch)
    return payload

def display_scores(scores, table):
    payload = {
        "text": 'Current scores:',
        "attachments": [
            {
                "footer": 'Correct answer: 1 pt - First to give it: 2 pts - Wrong answer: 0 pt',
                "mrkdwn_in": ["text"],
                "color": "#36a64f",
                "fields": []
            }
        ]
    }

    for i, (user, sc) in enumerate(scores.items()):
        option = {'title': '%s. %s (%s pts)'%(i+1, table[user], sc),
            'short': False}
        payload['attachments'][0]['fields'].append(option)


    return payload

def solve_question(question, replies):

    text, options, correct, author = question
    counts = {}
    total_right = 0

    for i, (user, has_correct, index) in enumerate(replies):
        opt = "ABCDEFGH"[index]
        counts.setdefault(opt, 0)
        counts[opt] = counts[opt] + 1
        if has_correct:
            total_right = total_right + 1

    total_n = sum(list(counts.values()))

    pc = total_right / float(total_n)*100 if total_n != 0 else 'n/a'

    answers = []
    if pc != 'n/a':
        for j in range(0, len(options)):
            opt = "ABCDEFGH"[j]
            n = 0
            if opt in list(counts.keys()):
                n = counts[opt]

            option = '%s. %s (%s %%)'%(opt, n, n/float(total_n)*100)
            answers.append(option)


    footer = "%s - %s answered right (%s %%)"\
        %(' - '.join(answers), total_right, pc)

    if not str(correct).isdigit():
        correct = 'ABCDEFGH'.index(correct.upper())
    right = '*%s. %s*'%('ABCDEFGH'[correct], options[correct])

    payload = {
        "text": 'Time is over. The right answer was: %s.'%right,
        "attachments": [
            {
                "footer": footer,
                "mrkdwn_in": ["text"],
                "color": "#36a64f",
                "fields": []
            }
        ]
    }

    return payload
