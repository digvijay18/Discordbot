import os
from bot import TesterBot
from commands import WebCommands

from dotenv import load_dotenv

load_dotenv()

token = os.getenv('DISCORD_TOKEN')

if __name__ == '__main__':
    bot = TesterBot(command_prefix="!")
    commands = WebCommands()
    bot.register_commands(commands)
    bot.run(token)
