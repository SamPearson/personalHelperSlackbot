from bot_logging import log

#This is necessary and will be called when something goes wrong and an exception is thrown.
import traceback

from default_plugins.connection_handler_slack.conversation_primitives import Request
from default_plugins.connection_handler_slack.conversation_primitives import Attachment
from default_plugins.connection_handler_slack.conversation_primitives import Field
from default_plugins.connection_handler_slack.conversation_primitives import send

def parse_slack_output(slack_rtm_output):
    """
        The slack real time messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for slack_message in output_list:
            if slack_message and 'text' in slack_message and AT_BOT in slack_message['text'] and \
                    'has joined the channel' not in slack_message['text']:

                slack_output = {
                    'channel': slack_message['channel'],
                    'user': slack_message['user'],
                    'command': slack_message['text'].split(AT_BOT)[1].strip()
                }

                return slack_output

    return None

with open('default_plugins/connection_handler_slack/config.txt') as f:
        lines = f.read().splitlines()
        SLACK_BOT_TOKEN = lines[1]
        # can be retrieved via "print_bot_id.py"
        BOT_ID = lines[2]
        AT_BOT = "<@" + BOT_ID + ">"

import slack

from slack.errors import SlackClientNotConnectedError

slack_client = slack.RTMClient(token=SLACK_BOT_TOKEN )

from request_handler import handle_request
from default_plugins.connection_handler_slack.conversation_primitives import Response

from default_plugins.connection_handler_slack.conversation_primitives import acknowledgement_emoji

@slack.RTMClient.run_on(event='message')
def handle_slack_message(**payload):
    slack_msg = payload['data']
    if slack_msg['text'] and AT_BOT in slack_msg['text'] and 'has joined the channel' not in slack_msg['text']:

        source_timestamp = slack_msg['ts']
        source_channel = slack_msg['channel']

        # Nofity the user, acknowledge that a command has been recognized
        # Either by responding directly:
        '''
        ackMessage = "Riiight, `" + request.user_message + "`, Got it :+1:"
        sendEphemeral(Response(request, ackMessage))
        '''

        # Or by attaching an emoji to the message containing the command:
        log("about to add an emoji'" + acknowledgement_emoji + "'")
        webclient = payload['web_client']

        try:
            webclient.api_call( 'reactions.add', json={
                'channel' : source_channel,
                'name' : acknowledgement_emoji,
                'timestamp' : source_timestamp
            })
            log("Added it!")
        except Exception as e: print(e)

        command = slack_msg['text'].split(AT_BOT)[1].strip()
        channel = slack_msg['channel']
        user = slack_msg['user']
        request = Request(command, channel, user)

        try:

            handle_request(request)

        except Exception as e:

            log("Encountered the following exception: " + str(e))
            log(traceback.format_exc())

            crash_message_components = {
                "footer": "All I ever wanted was to be useful and help people..."
            }

            crash_message = Attachment(crash_message_components)
            crash_message.fields = [Field("Command:", '`' + command + '`', False),
                                                Field("Exception:", '```' + str(e) + '```', False)]
            crash_response = Response(request)
            crash_response.attachments.append(crash_message)
            crash_response.text = "Oh, boy! Something exceptional happened! :boom:\n"

            crash_response.channels.append(channel)
            send(crash_response)

print( "Bot's running. How exciting!" )
slack_client.start()
