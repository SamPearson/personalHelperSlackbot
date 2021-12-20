from default_plugins.connection_handler_slack.conversation_primitives import send
from bot_logging import log

from default_plugins.connection_handler_slack.conversation_primitives import Response
from default_plugins.connection_handler_slack.conversation_primitives import Attachment
from default_plugins.connection_handler_slack.conversation_primitives import Field

import sys

'''
Plugins can be created by implementing subclasses of the Command class below.
plugin commands should override the execute method but keep the provided detect
method.
'''
class Command:
    name = ""
    invocations = []
    description = ""
    usage_example = ""
    help_text = ""

    def __init__(self):
        print("")

    # Plugin commands should override this
    def execute(self):
        log("the default execute() method was called from a command: '" + self.name + "'")

    def detect(self, request):
        for v in self.invocations:
            if request.user_message.startswith(v):

                request.command = self.name
                l = len(v)
                request.parameter_string = request.user_message[l:].lstrip()

                return True

        return False

    # Provides command usage info, invocations, etc from slack
    def get_help_card(self):

        help_card = Attachment(
            {"title": self.name,
             "title_link": "https://i.imgur.com/Lmvmfkd.jpg", "footer": "Command and Conquer!"})

        help_card.fields.append(Field("Description", self.description, False))

        invocation_list = "`" + "`, `".join(self.invocations) + "`"
        help_card.fields.append(Field("Invocations", invocation_list, False))

        help_card.fields.append(Field("Example", "`" + self.usage_example + "`", False))

        if self.help_text != "":
            help_card.fields.append(Field("Help!", self.help_text, False))

        return help_card


'''
An example of implementing a command via inheriting from the Command class.

name, description, invocations, usage_example, and help_text will all be shown
when the user runs the help command against a command you provide.

The execute function will be run when the command is called, so it's overridden
here.
'''
class GreetingCommand(Command):
    def __init__(self):
        self.name = "Greeting"
        self.description = "Say hi! The bot says hi!"
        # Invocations are the way you activate the command. If your command starts with one of the invocations,
        # the execute() method will be called. Be careful of short invocations, they may get triggered accidentally.
        self.invocations = ["hi!",
                            "hi ",
                            "hello",
                            "hey"
                            ]
        self.usage_example = "@bot hi!"
        self.help_text = " - It's always a great day!\n" \
                         " - Sometimes when you say hi real people don't say hi back," \
                         " you need to be prepared for that\n"

    def execute(self, request):
        send(Response(request, "Hi there! You've activated the `" + self.name + "` command!"))
