from bot_logging import log
from bot_logging import log_break
import re

import json
from pprint import pprint

import slack

acknowledgement_emoji = "robot_face"

with open('./default_plugins/connection_handler_slack/config.txt') as f:
    lines = f.read().splitlines()
    SLACK_BOT_TOKEN = lines[1]
    SLACK_BOT_NAME = lines[0]
    # can be retrieved via "print_bot_id.py"
    BOT_ID = lines[2]
    AT_BOT = "<@" + BOT_ID + ">"
    for l in lines:
        if "emoji" in l:
            acknowledgement_emoji = l[l.index("=")+1:]

slack_client = slack.WebClient(SLACK_BOT_TOKEN)


def send(response):

    response.channels = set(response.channels)  # de-dupe to prevent double-posting
    for chan in response.channels:  # who is this for chan
        log("This channel was listed as one to post to: " + chan)

        r = slack_client.api_call( response.slack_api_endpoint, json={
            'channel' : chan,
            'text' : response.text,
            'attachments' : response.get_attachment_json(),
            'user' : response.request_author,
            'username' : SLACK_BOT_NAME,
            'icon_emoji' : acknowledgement_emoji,
            'as_user' : False

        })


        # The slack API returns a json blob with 'r' set to 'ok'
        # unless the call has failed.
        if not r['ok']:
            pprint(r)
            log("The response didn't come back 'ok'")
            print("The text: " + response.text)
            print("The attachments:")
            print(response.get_attachment_json())
            log("RESPONSE: FAILED")


# Ephemeral messages are only shown to the user whom they are a reply to.
def sendEphemeral(response):
    response.slack_api_endpoint = "chat.postEphemeral"
    origin_channel = [response.channels[0]]
    response.channels = origin_channel

    send(response)


class Response:

    def __init__(self, req, t=""):
        self.attachments = []
        self.text = t
        self.channels = [req.channel_id]
        self.request_author_slack_id = req.author_slack_id
        self.request_author = req.author_slack_id
        self.slack_api_endpoint = "chat.postMessage"

    def get_attachment_json(self):
        attachment_json = []
        for a in self.attachments:
            attachment_json.append(a.get_json())

        return attachment_json


class Request:

    def __init__(self, raw, slack_channel_id, slack_id):
        self.user_message = raw.lower()
        self.command = ""
        self.parameter_string = ""
        self.channel_id = slack_channel_id
        self.channel = ""
        self.author = slack_id
        self.author_slack_id = slack_id

        # Start a log entry for this instance of handling input
        log_break()
        log("Someone atted the bot, looking into it.")
        log("The full message was: " + self.user_message)

        '''
        Requests may have 'quoted arguments' eg -newTitle"The new title"
        This is done by using regex to find substrings that:
            - start with a hyphen
            - followed by any number of capital or lowercase letters (in the example above, "newTitle")
            - followed by a quotation mark
            - followed by any number of any character except a quotation mark (in the above example: The new title)
            - followed by a quotation mark
        '''
        self.quoted_arguments = {}
        if  '"' in self.user_message:
            quoted_arguments = re.findall( "-[aA-zZ]*\"[^\"]*\"", self.user_message)
            for qa in quoted_arguments:
                log("Found a quoted argument: " + qa)
                first_quotation_mark_position = qa.find('"')
                argument_key = qa[1:first_quotation_mark_position]
                argument_value = qa[first_quotation_mark_position+1:-1]
                self.quoted_arguments.update( { argument_key : argument_value})
                log("Successfully logged the value of '" + argument_key + "' as '" + argument_value + "'")
                self.user_message = self.user_message.replace(qa,"")


class Field:
    def __init__(self, title, value, short=True):
        self.title = title
        self.value = value
        self.short = short

    def get_json(self):

        json_dict = {"title": self.title,
                     "value": self.value,
                     "short": self.short}

        json_string = json.dumps(json_dict)

        return json.loads(json_string)


class Attachment:

    def __init__(self, components):
        if 'color' in components:
            self.color = components['color']
        else:
            self.color = "#00cccc"

        if 'pretext' in components:
            self.pretext = components['pretext']

        if 'text' in components:
            self.text = components['text']
        else:
            self.text = ""

        if 'author_name' in components:
            self.author_name = components['author_name']

        if 'author_byline' in components:
            self.author_byline = components['author_byline']

        if 'title' in components:
            self.title = components['title']
        else:
            self.title = ""

        if 'title_link' in components:
            self.title_link = components['title_link']
        else:
            self.title_link = ""

        if 'fields' in components:
            self.fields = components['fields']
        else:
            self.fields = []

        if 'footer' in components:
            self.footer = components['footer']
        else:
            self.footer = ""

    def get_json(self):

        json_dict = {
            "text": self.text,
            "color": self.color,
            "title": self.title,
            "title_link": self.title_link,
            "footer": self.footer
        }

        fields = []
        for f in self.fields:
            fields.append(f.get_json())

        json_dict["fields"] = fields

        # Turn the dictionary into a string
        json_string = json.dumps(json_dict)
        # Turn the string into json
        return json.loads(json_string)
