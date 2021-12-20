import os
import slack

with open('config.txt') as f:
    lines = f.read().splitlines()
    BOT_NAME = lines[0]
    SLACK_BOT_TOKEN = lines[1]

print( BOT_NAME )
print( SLACK_BOT_TOKEN )


slack_client = slack.WebClient( SLACK_BOT_TOKEN )
print( "Connection established" )
if __name__ == "__main__":
    api_call = slack_client.api_call("users.list")
    if api_call.get('ok'):
        # retreive all users so we can find our bot
        users = api_call.get('members')
        for user in users:
            if 'name' in user and user.get('name') == BOT_NAME:
                print("Bot ID for '" + user['name'] + "' is " + user.get('id'))
    else:
        print("could not find bot user with the name " + BOT_NAME)

