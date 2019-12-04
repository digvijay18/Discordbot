import os
from app.bot import TesterBot
from app.commands import WebCommands

from dotenv import load_dotenv

load_dotenv()

token = os.getenv('DISCORD_TOKEN')


def application():
    """
    This is the entry point for the application. This function instantiates the
    bot. Then, it loads the commands module. Commands are abstracted away so that
    they can be classified (for example search commands that employ web for the
    purpose of this app. Once we register the command set, the commands defined
    in the loaded module are available exactly for usage on bot. After registration,
    we run the bot.
    """
    bot = TesterBot(command_prefix="!")
    bot.register_commands(WebCommands)
    bot.run(token)
