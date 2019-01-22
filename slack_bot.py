#!/usr/bin/env python
# -*- coding: utf-8 -*-
from slackclient import SlackClient
import time, re, operator, boto3, json, sys

KARMA_ACTION = re.compile(r'(?:^| )(\S{2,}?)\s?([\+\-]{2,})')
slack_token = "YOUR_SLACK_TOKEN"
sc = SlackClient(slack_token)

session = boto3.Session(
    aws_access_key_id="KEY",
    aws_secret_access_key="ACCESS_KEY",
)

s3 = session.resource('s3')
s3object = s3.Object('Bucket','data.json')
users_karma = json.loads(s3object.get()['Body'].read())

def main_loop():
    if sc.rtm_connect(with_team_state=False):
        while True:
            events = sc.rtm_read()
            for event in events:
                if ('channel' in event and event.get('type') == 'message' and 'text' in event):
                    text = event['text']
                    channel = event['channel']
                    user = "<@" + event['user'] + ">"
            
                    if text == "!karma top":
                        list_karma = sorted(users_karma.items(), key=operator.itemgetter(1), reverse=True)
                        top_count = 0
                        top_karma_message = "Top Karma Users: \n"
                        for v,k in list_karma:
                            top_count = top_count + 1
                            if top_count > 10:
                                break
                            else:
                                top_karma_message = top_karma_message + str(top_count) + "- " + str(v) + " with " + str(k) + " karma. \n"
                        sc.rtm_send_message(channel, top_karma_message)
                        continue

                    elif text == "!karma":
                        sc.rtm_send_message(channel, user + "'s karma is " + str(users_karma[user]))
                        continue

                    karma_changes = KARMA_ACTION.findall(text)
                    if not karma_changes:
                        continue
                    else:
                        for karma in karma_changes:
                            print("action: " + karma[1])
                            print("user: " + karma[0])
                            if len(karma[0]) < 2:
                                continue
                            if user in text:
                                sc.rtm_send_message(channel, "❌ You can't vote for yourself ❌")
                                continue
                            if "++" in karma[1]:
                                to_add = len(karma[1]) - 1
                                if len(karma[1]) >= 5:
                                    to_add = 5
                                    sc.rtm_send_message(channel, "💥 :parrot: 💥  :parrot: 💥  :parrot: 💥  ")
                                if karma[0] in users_karma:
                                    users_karma[karma[0]] = users_karma[karma[0]] + to_add
                                else:
                                    users_karma[karma[0]] = to_add
                            elif "--" in karma[1]:
                                to_rm = len(karma[1]) - 1
                                if len(karma[1]) >= 5:
                                    to_rm = 5
                                    sc.rtm_send_message(channel, "💀 :parrot: 💀  :parrot: 💀  :parrot: 💀  ")
                                if karma[0] in users_karma:
                                    users_karma[karma[0]] = users_karma[karma[0]] - to_rm
                                else:
                                    users_karma[karma[0]] = 0 - to_rm

                            sc.rtm_send_message(channel, karma[0] + "'s karma is now at " + str(users_karma[karma[0]]))
                            s3object.put(
                                Body=(bytes(json.dumps(users_karma).encode('UTF-8')))
                            )
        time.sleep(1)
    else:
        print("Connection Failed")

if __name__ == '__main__':
    try:
        main_loop()
    except KeyboardInterrupt:
        sys.exit(0)
