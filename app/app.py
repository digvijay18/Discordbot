import os
from app.bot import TesterBot
from app.commands import WebCommands

from dotenv import load_dotenv

load_dotenv()

token = os.getenv('DISCORD_TOKEN')


def application():
    bot = TesterBot(command_prefix="!")
    commands = WebCommands()
    bot.register_commands(commands)
    bot.run(token)
