# Copyright (c) 2017 Blemundsbury AI Limited
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import sys, time
from slackclient import SlackClient
from cape.client import CapeClient, CapeException


CAPE_TOKEN = 'myusertoken' # Your Cape user token
SLACK_KEY = 'myslackkey' # Your bot's Slack key
BOT_ID = 'mybotid' # Your bot's Slack ID
READ_WEBSOCKET_DELAY = 1 # Delay in seconds between reading from firehose


cc = CapeClient()


def handle_question(question, channel, bot, slack_client):
    answers = cc.answer(question, CAPE_TOKEN)
    if len(answers) > 0:
        slack_client.api_call("chat.postMessage", channel=channel,
                              text="%s (confidence: %0.2f)" % (answers[0]['answerText'], answers[0]['confidence']), as_user=True)
    else:
        slack_client.api_call("chat.postMessage", channel=channel,
                              text="Sorry! I don't know the answer to that.", as_user=True)


def parse_slack_output(slack_rtm_output, bot):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            at_bot = "<@%s>" % BOT_ID
            if output and 'text' in output and at_bot in output['text'] and 'channel' in output:
                # return text after the @ mention, whitespace removed
                return output['text'].split(at_bot)[1].strip(), \
                       output['channel']
    return None, None


if __name__ == "__main__":
    client = SlackClient(SLACK_KEY)
    if client.rtm_connect():
        print("Connected")
    else:
        print("Failed to connect")
        sys.exit()

    while True:
        message, channel = parse_slack_output(client.rtm_read(), bot)
        if message and channel:
            handle_question(message, channel, bot, client)
        time.sleep(READ_WEBSOCKET_DELAY)
