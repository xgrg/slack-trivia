# slack-trivia

[![pipeline status](https://img.shields.io/travis/xgrg/slack-trivia.svg)](https://travis-ci.org/xgrg/slack-trivia)
[![pipeline Status](https://coveralls.io/repos/github/xgrg/slack-trivia/badge.svg?branch=master)](https://coveralls.io/github/xgrg/slack-trivia?branch=master)


`slack-trivia` is yet another integration for Slack workspaces to run quizzes (multiple choice questions) in a Slack channel. This runs as a Python script and is
based on the Slack Python API.

<img src="https://raw.githubusercontent.com/xgrg/slack-trivia/master/doc/images/img1.png" width=500>

## Requirements

- Slack bot - instructions on how to create one at https://api.slack.com/bot-users
- Python v3.7+

## Getting started

1. Clone or download the repository into a local folder.
2. Add this folder to your `$PYTHONPATH`.
3. Create an environment variable `TOKEN` with the bot token.
4. Edit `quizz.py` and define `su` as a list of user IDs who will be allowed to
operate the bot commands (hint: add the bot name)
5. Run `python quizz.py`

## Available commands

All users in same channel as the bot may play and answers questions.
The following commands are for superusers only.

`!quizz [channel]` : post random question in given channel and wait for answers

`!next [channel]` : solve question and display scores

`!create question [option_a, option_b, .., option_x] correct_letter` : create a
new question and adds it to the database

<img src="https://raw.githubusercontent.com/xgrg/slack-trivia/master/doc/images/img2.png" width=500>

`!scores` : display current scores

`!scores_reset` : reset current scores

`!json` : export current questions in a JSON file

`!table` : display the workspace's user table

## Cron

The [`cron`](https://github.com/xgrg/slack-trivia/blob/master/cron) script allows to send `!quizz` and `!next` commands to the bot
at a given frequency so that questions are asked and solved automatically.
Run it in parallel of `quizz.py`.
