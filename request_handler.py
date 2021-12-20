
from bot_logging import log
from default_plugins.genericbot import generic_bot_commands
import custom_plugins

from default_plugins.connection_handler_slack.conversation_primitives import send
from default_plugins.connection_handler_slack.conversation_primitives import Response
from default_plugins.connection_handler_slack.conversation_primitives import Attachment
from default_plugins.connection_handler_slack.conversation_primitives import Field


command_classes = generic_bot_commands.Command.__subclasses__()
commands = []
for c in command_classes:
    commands.append(c())

def handle_request(request):

    log("The message from the user was : '" + request.user_message + "'")

    message = request.user_message.lower()
    if message.startswith("help"):
        help_response = Response(request)

        for command in commands:

            if command.name.lower() in message.lower():
                help_response.attachments.append(command.get_help_card())
            else:
                for invocation in command.invocations:
                    if invocation in message:
                        help_response.attachments.append(command.get_help_card())

        if len(help_response.attachments) == 0:
            help_response.text = "Here's a list of commands, try sending `help COMMAND_NAME` " \
                                 "or if `help COMMAND_INVOCATION` you know any of the command's invocations"

            attachment_list = []
            for command in commands:
                attachment_list.append(Attachment({
                    "title": command.name,
                    "text": command.description
                }))

            help_response.attachments = attachment_list


        send(help_response)

    for command in commands:
        if command.detect(request):
            command.execute(request)
