#!/usr/bin/env python3
"""Telegram bot for Thoughts & Prayers.

Build it with: docker build -f Dockerfile.telegram -t telegram-tap .
Run it with something like: docker run -ti --rm -e TAPBOT_TOKEN=your-telegram-token telegram-tap

Copyright 2018-2021 Davide Alberani <da@erlug.linux.it> Apache 2.0 license
"""

import os
import sys
import logging
import subprocess
from telegram.ext import Updater, CommandHandler

sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def getThoughtsAndPrayers():
    cmd = ['/cry-a-lot']
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    try:
        stdout = stdout.strip()
        stdout = stdout.decode('utf8')
    except:
        return 'uh-oh: something was wrong with the encoding of the prayer; try again'
    if process.returncode != 0:
        return 'something terrible is happening: exit code: %s, stderr: %s' % (
                process.returncode, stderr.decode('utf8'))
    if not stdout:
        return 'sadness: the Thoughts & Prayers bottle was empty; try again'
    return stdout


def tap(bot, update):
    a_tap = getThoughtsAndPrayers()
    logging.info('%s wants some Thoughts & Prayers; serving:\n%s' % (bot.effective_user.username, a_tap))
    bot.message.reply_text(a_tap)


def about(bot, update):
    logging.info('%s required more info' % bot.effective_user.username)
    bot.message.reply_text('See https://github.com/alberanid/thoughts-and-prayers')


if __name__ == '__main__':
    if 'TAPBOT_TOKEN' not in os.environ:
        print("Please specify the Telegram token in the TAPBOT_TOKEN environment variable")
    logging.info('start serving Thoughts & Prayers')
    updater = Updater(os.environ['TAPBOT_TOKEN'])
    updater.dispatcher.add_handler(CommandHandler('tap', tap))
    updater.dispatcher.add_handler(CommandHandler('about', about))
    updater.start_polling()
    updater.idle()
