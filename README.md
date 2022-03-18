# Personal Helper Bot

A general purpose slackbot to automate the boring stuff


A configuration file is needed to run the bot.
It needs to be created manually, at this location:

./default_plugins/connection_handler_slack/config.txt

This file needs a few pieces of information, one per line. The first line should be the name of the bot.

The second line should be the the api token. To get that:
Go here: https://api.slack.com/apps
(create an app if one has not been created)
Click on the app 
If the bot has been installed to your workspace, you should see a bot user OAuth token it should start with "xoxb-"

The third line should be the bot user's "id", which can be retrieved by running print_bot_id.py from this directory:
./default_plugins/connection_handler_slack


Launching the bot:

Currently, the bot needs to be run from a python environment with
various modules installed.
With the virtual environment activated, simply run
$ python main.py

You should get a message like:

Bot's running. How exciting!


At which point the bot is running and ready to accept commands in slack.
"Help" is the only default command; you'll need to install or build plugins
to make the bot more useful.

To create plugins:
 - Create a new folder under the "custom_plugins" folder. Name it whatever you want
 - Create a file in the plugin folder, again name it whatever you want
 - Copy the example from default_plugins/genericbot/generic_bot_commands.py
 - paste it into custom_plugins/whatever_you_want/whatever_you_want.py
 - Edit the class name
 - Start off by providing a usage example, build help text as you build the command
