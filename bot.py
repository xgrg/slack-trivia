from payload import *
from functions import *
import json, random

def on_reply(payload, trivia):
    data, sender = trivia.get_params(payload)
    print('REPLY from %s'%sender)

    reply = data['text'].upper()
    index = 'ABCDEFGH'.index(reply)
    text, options, correct, author = trivia.pending_question

    if index > len(options):
        msg = 'Invalid answer. Please check possible options.'
        response = trivia.post_text(msg, sender)

        payload = create_question(text, options, author)
        response = trivia.post(payload, sender)
        return
    elif sender in [r[0] for r in trivia.replies]:
        msg = 'Your answer was already registered. Please wait for the solution.'
        response = trivia.post_text(msg, sender)
        return

    reply = create_reply(text, options, correct, reply, author)
    r = [sender, index==correct, index]
    trivia.replies.append(r)
    trivia.dump()

    response = trivia.post(reply, sender)

def on_next(payload, trivia):
    print('NEXT')
    data, sender = trivia.get_params(payload)

    user = get_user_id(trivia.webclient, 'goperto')
    args = data['text'].split('!next')[1]
    target = 'bottest'
    if len(args.strip(' ')) > 1:
        target = args.strip(' ')
    print('TARGET: %s'%target)
    channel = get_channel_id(trivia.webclient, target)

    if user != data['user']:
        print('User %s not authorized'%trivia.table[sender])

    if len(trivia.replies) == 0:
        msg = 'No answers to this question.'
        response = trivia.post_text(msg, channel)
    else:

        trivia.scores.setdefault(trivia.replies[0][0], 0)
        if trivia.replies[0][1]:
            trivia.scores[trivia.replies[0][0]] += 2
        for r in trivia.replies[1:]:
            trivia.scores.setdefault(r[0], 0)
            if r[1]:
                trivia.scores[r[0]] += 1



    payload = solve_question(trivia.pending_question, trivia.replies)
    response = trivia.post(payload, channel)

    trivia.replies = []
    trivia.pending_question = None
    trivia.dump()

    payload = display_scores(trivia.scores, trivia.table)
    response = trivia.post(payload, channel)
    msg = 'Next question in 24 hours...'
    response = trivia.post_text(msg, channel)


def on_quizz(payload, trivia):
    print('QUIZZ')
    data, sender = trivia.get_params(payload)

    trivia.table = get_users_table(trivia.webclient)
    # user = get_user_id(trivia.webclient, "goperto")
    # user1 = get_user_id(trivia.webclient, "quizzbot")
    #
    # if not sender in [user, user1]:
    #     print(sender)
    #     print('User %s not authorized'%trivia.table[sender])

    questions = json.loads(''.join(open('questions.json').read().split('\n')))

    qno = random.randrange(0, len(questions))
    while qno == trivia.previous:
        qno = random.randrange(0, len(questions))
    trivia.previous = qno

    text, options, correct, author = questions[qno]

    payload = create_question(text, options, author)
    trivia.replies = []

    args = data['text'].split('!quizz')[1]
    target = 'bottest'
    if len(args.strip(' ')) > 1:
        target = args.strip(' ')
    channel = get_channel_id(trivia.webclient, target)

    response = trivia.post(payload, channel)

    trivia.pending_question = questions[qno]
    channel, ts = response['channel'], response['ts']
    #trivia.dump()


def on_ping(payload, trivia):
    print('PING')
    data, sender = trivia.get_params(payload)

    text, options, correct, author = trivia.pending_question
    payload = create_question(text, options, author)

    response = trivia.post(payload, sender)


def on_create(payload, trivia):
    print('CREATE')
    data, sender = trivia.get_params(payload)
    if not hasattr(trivia, 'table'):
        trivia.table = get_users_table(trivia.webclient)

    try:
        text = data['text'].split('!create ')[1]
        question = text.split('[')[0]
        options = text[text.index('[') + 1: text.index(']')].split(',')
        correct = text[text.index(']') +1:].strip(' ')
        try:
            index = int(correct)
            correct = options[index]
        except ValueError:
            letters = ['a','b','c','d','e','f','g']
            if correct.lower() in letters:
                correct = options[letters.index(correct.lower())]
        payload = create_question(question, options, sender)

        letter = 'ABCDEFGH'[index]
        msg = 'Correct answer is *%s. %s*'%(letter, correct)
        response = trivia.post(payload, sender)
        response = trivia.post_text(msg, sender)

    except Exception as e:
        print(e)
        msg = 'Format error. Format: `!create` _type your question_ [_option1_, _option2_, _option3_, _option4_] _correct index_.'
        payload = {
            "text": msg,
            "attachments": [{
                    "text": "Ex: `!create` _What is the best research group in the world? [VuMC, RCBB, CCRB, BBRC] 3_"
                    }]
        }
        response = trivia.post(payload, sender)
        return

    questions = json.loads(''.join(open('questions.json').read().split('\n')))
    qno = random.randrange(0, len(questions))
    questions.append([question, options, index, trivia.table[sender]])
    json.dump(questions, open('questions.json', 'w'), indent=2)
    msg = 'Question has been correctly registered! Question #%s.'%len(questions)
    response = trivia.post_text(msg, sender)

def on_json(payload, trivia):
    print('JSON')
    data, sender = trivia.get_params(payload)
    trivia.webclient.files_upload(file='questions.json', channels='@goperto')
