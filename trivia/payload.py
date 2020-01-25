import string

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
    for each, letter in zip(options, string.ascii_uppercase):
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

    for each, letter in zip(options, string.ascii_uppercase):
        option = {'title': '%s. %s'%(letter, each), 'short': False}
        payload['attachments'][0]['fields'].append(option)

    index = string.ascii_uppercase.index(reply)
    print(reply)
    print(options[index])

    attch = {"mrkdwn_in": ["text"],
        "color": "#36a64f",
        "text": 'You replied: _%s. %s_'%(reply, options[index])}

    payload['attachments'].append(attch)
    if reply == correct:
        attch = {"mrkdwn_in": ["text"],
            "color": "#36a64f",
            "pretext": 'CORRECT!'}
        payload['attachments'].append(attch)
    else:
        index = string.ascii_uppercase.index(correct)
        print(correct)
        print(options[index])
        attch = {"mrkdwn_in": ["text"],
            "color": "#36a64f",
            "text": 'The right answer was: *%s. %s*'%(correct, options[index])}
        payload['attachments'].append(attch)
    print(payload)
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

    import operator
    sorted_scores = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)

    for i, (user, sc) in enumerate(sorted_scores):
        a = '%s.\t'%(i + 1) if i == 0 or sc != old else '\t'
        option = {'title': '%s%s (%s pts)'%(a, table.get(user, 'unknown'), sc),
            'short': False}
        old = sc
        payload['attachments'][0]['fields'].append(option)
    return payload

def solve_question(question, replies):

    text, options, correct, author = question
    counts = {}
    total_right = 0
    print(replies)

    for i, (user, has_correct, reply) in enumerate(replies):
        counts.setdefault(reply, 0)
        counts[reply] = counts[reply] + 1
        if has_correct:
            total_right = total_right + 1

    total_n = sum(list(counts.values()))

    pc = total_right / float(total_n)*100 if total_n != 0 else 'n/a'

    answers = []
    if pc != 'n/a':
        for j in range(0, len(options)):
            opt = string.ascii_uppercase[j]
            n = 0
            if opt in list(counts.keys()):
                n = counts[opt]

            option = '%s. %s (%s %%)'%(opt, n, n/float(total_n)*100)
            answers.append(option)

    footer = "%s - %s answered right (%s %%)"\
        %(' - '.join(answers), total_right, pc)

    index = string.ascii_uppercase.index(correct)
    right = '*%s. %s*'%(correct, options[index])

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
