#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
from mastodon import Mastodon

API_URL = 'https://botsin.space/'

sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)

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


def serve(token):
    tap = getThoughtsAndPrayers()
    print('my thoughts & prayers: %s' % tap)
    mastodon = Mastodon(access_token=token, api_base_url=API_URL)
    mastodon.status_post(tap)


if __name__ == '__main__':
    if 'TAPBOT_TOKEN' not in os.environ:
        print("Please specify the Mastodon token in the TAPBOT_TOKEN environment variable")
        sys.exit(1)
    serve(token=os.environ['TAPBOT_TOKEN'])
