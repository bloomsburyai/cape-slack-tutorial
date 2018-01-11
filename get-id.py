#!/usr/bin/env python3
import os, sys
from slackclient import SlackClient

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: ./get-id.py slack-key bot-name")
        sys.exit(1)
    slack_key = sys.argv[1]
    bot_name = sys.argv[2]
    slack_client = SlackClient(slack_key)
    api_call = slack_client.api_call("users.list")
    if api_call.get('ok'):
        users = api_call.get('members')
        for user in users:
            if user['name'].lower() == bot_name.lower():
                print("ID for '%s' is %s" % (user['name'], user.get('id')))
                sys.exit()
        print("Couldn't find %s" % bot_name)
