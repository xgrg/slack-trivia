from trivia import payload as pl
from trivia import functions as func
from trivia import bot
import json, random, string, os, sys

def on_message(payload, trivia):
    data = payload['data']

    if 'text' not in data:
        print('text not in data')
        return

    text = data['text'].strip(' ')
    sender = data['user']
    sender_name = trivia.get_username(data['user'])
    print('Message from %s (%s)'%(sender_name, sender))

    if not trivia.pending_question is None:
        print('PENDING QUESTION DETECTED')
        if text.upper() in string.ascii_uppercase and len(text) == 1:
            bot.on_reply(payload, trivia)

        elif text.startswith('!next') and sender_name in trivia.su:
            bot.on_next(payload, trivia)

        elif text == '!':
            bot.on_ping(payload, trivia)

    else:
        print('NO PENDING QUESTION')
        if text.startswith('!quizz') and sender_name in trivia.su:
            bot.on_quizz(payload, trivia)

    if text.startswith('!create'):
        bot.on_create(payload, trivia)
        bot.on_json(payload, trivia)

    elif text.startswith('!json') and sender_name in trivia.su:
        bot.on_json(payload, trivia)

    elif text == '!scores' and sender_name in trivia.su:
        bot.on_scores(payload, trivia)

    elif text == '!scores_reset' and sender_name in trivia.su:
        bot.on_scores_reset(payload, trivia)

    elif text == '!quit' and sender_name in trivia.su:
        sys.exit(0)

    else:
        print('ELSE')
        #print(payload)

def on_reply(payload, trivia):
    data, sender = trivia.get_params(payload)
    sender_name = trivia.get_username(sender)
    print('Reply from %s (%s)'%(sender_name, sender))

    reply = data['text'].upper()
    index = string.ascii_uppercase.index(reply)

    text, options, correct, author = trivia.pending_question

    if sender in [r[0] for r in trivia.replies]:
        msg = 'Your answer was already registered. Please wait for the solution.'
        trivia.post_text(msg, sender)
        return
    elif index > len(options) - 1:
        msg = 'Invalid answer. Please check possible options.'
        trivia.post_text(msg, sender)

        payload = pl.create_question(text, options, author)
        trivia.post(payload, sender)
        return

    rep = pl.create_reply(text, options, correct, reply, author)
    r = [sender, reply==correct, reply]
    trivia.replies.append(r)
    trivia.post(rep, sender)


def on_next(payload, trivia):
    data, sender = trivia.get_params(payload)
    sender_name = trivia.get_username(sender)
    print('Next from %s (%s)'%(sender_name, sender))

    args = data['text'].split('!next')[1]
    target = 'bottest'
    if len(args.strip(' ')) > 1:
        target = args.strip(' ')
    print('TARGET: %s'%target)
    channel = None
    if not 'CI_TEST' in os.environ:
        channel = func.get_channel_id(trivia.webclient, target)

    if len(trivia.replies) == 0:
        msg = 'No answers to this question.'
        trivia.post_text(msg, channel)
    else:
        is_first = True
        trivia.scores.setdefault(trivia.replies[0][0], 0)
        if trivia.replies[0][1]:
            trivia.scores[trivia.replies[0][0]] += 2
            is_first = False

        for r in trivia.replies[1:]:
            trivia.scores.setdefault(r[0], 0)
            if r[1]:
                if is_first:
                    trivia.scores[r[0]] += 1
                    is_first = False
                trivia.scores[r[0]] += 1

    payload = pl.solve_question(trivia.pending_question, trivia.replies)
    trivia.post(payload, channel)

    trivia.replies = []
    trivia.pending_question = None

    payload = pl.display_scores(trivia.scores, trivia.table)
    trivia.post(payload, channel)
    msg = 'Next question will come later…'
    trivia.post_text(msg, channel)


def on_quizz(payload, trivia):
    data, sender = trivia.get_params(payload)
    sender_name = trivia.get_username(sender)
    print('Quizz started by %s (%s)'%(sender_name, sender))


    questions = json.loads(''.join(open(trivia.fp).read().split('\n')))

    qno = random.randrange(0, len(questions))
    while qno == trivia.previous:
        qno = random.randrange(0, len(questions))
    trivia.previous = qno

    text, options, correct, author = questions[qno]

    payload = pl.create_question(text, options, author)
    trivia.replies = []

    args = data['text'].split('!quizz')[1]
    target = 'bottest'
    if len(args.strip(' ')) > 1:
        target = args.strip(' ')

    channel = None
    if not 'CI_TEST' in os.environ:
        channel = func.get_channel_id(trivia.webclient, target)
    trivia.post(payload, channel)

    text, options, correct, author = questions[qno]
    if str(correct).isdigit():
        correct = string.ascii_uppercase[correct]
    else:
        correct = correct.upper()

    trivia.pending_question = (text, options, correct, author)


def on_ping(payload, trivia):
    data, sender = trivia.get_params(payload)
    sender_name = trivia.get_username(sender)
    print('Ping by %s (%s)'%(sender_name, sender))

    text, options, correct, author = trivia.pending_question
    payload = pl.create_question(text, options, author)

    trivia.post(payload, sender)


def on_create(payload, trivia):
    print(payload)
    data, sender = trivia.get_params(payload)
    sender_name = trivia.get_username(sender)
    print('Create by %s (%s)'%(sender_name, sender))


    if not hasattr(trivia, 'table') and not 'CI_TEST' in os.environ:
        trivia.table = func.get_users_table(trivia.webclient)

    try:
        text = data['text'].split('!create ')[1]
        question = text.split('[')[0]
        options = text[text.index('[') + 1: text.index(']')].split(',')
        correct = text[text.index(']') +1:].strip(' ')
        if str(correct).isdigit():
            index = int(correct)
            correct_text = options[index]
        elif correct.upper() in string.ascii_uppercase and len(correct) == 1:
            index = string.ascii_uppercase.index(correct.upper())
            correct_text = options[index]
        else:
            raise Exception('Format error. (%s, %s)'%(correct, options))
        payload = pl.create_question(question, options, sender)

        letter = correct.upper()
        msg = 'Correct answer is *%s. %s*'%(letter, correct_text)
        trivia.post(payload, sender)
        trivia.post_text(msg, sender)

    except Exception as e:
        print(e)
        msg = 'Format error. Format: `!create` _type your question_ [_option1_,'\
            ' _option2_, _option3_, _option4_] _correct index_.'
        payload = {
            "text": msg,
            "attachments": [{
                    "text": "Ex: `!create` _What is the best research group "\
                        "in the world? [VuMC, RCBB, CCRB, BBRC] 3_"
                    }]
        }
        trivia.post(payload, sender)
        return

    questions = json.loads(''.join(open(trivia.fp).read().split('\n')))
    if not 'CI_TEST' in os.environ:
        questions.append([question, options, index, trivia.table[sender]])
    json.dump(questions, open(trivia.fp, 'w'), indent=2)
    msg = 'Question has been correctly registered! Question #%s.'%len(questions)
    trivia.post_text(msg, sender)


def on_json(payload, trivia):
    print('JSON')
    data, sender = trivia.get_params(payload)
    if not 'CI_TEST' in os.environ:
        trivia.webclient.files_upload(file=trivia.fp, channels='@goperto')


def on_scores(payload, trivia):
    print('SCORES')
    data, sender = trivia.get_params(payload)

    if not hasattr(trivia, 'table'):
        trivia.table = {}
        if not 'CI_TEST' in os.environ:
            trivia.table = func.get_users_table(trivia.webclient)

    table = trivia.table

    payload = pl.display_scores(trivia.scores, table)
    trivia.post(payload, sender)


def on_scores_reset(payload, trivia):
    data, sender = trivia.get_params(payload)
    if not 'CI_TEST' in os.environ:
        trivia.scores = {}
    trivia.post_text('Reset scores. Done.', sender)
