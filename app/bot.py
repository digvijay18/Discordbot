"""
This file contains the bot class subclassed from discord.py arbitrary library.
"""


import os
import discord
from discord.ext.commands import Bot


from dotenv import load_dotenv

load_dotenv()

token = os.getenv('DISCORD_TOKEN')
server_name = os.getenv('DISCORD_SERVER_NAME')


class TesterBot(Bot):
    def register_commands(self, command_set):
        """
        This method registers the commands specified in the instantiated command
        class.
        """
        _commands = command_set.list_commands()
        for command in _commands:
            self.add_command(command)

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    async def on_error(self, event, *args, **kwargs):
        context, exception = args
        with open('err.log', 'a') as f:
            if event == 'on_message':
                f.write('Unhandled message: %s\n' % str(exception))
            else:
                f.write('Unknown Exception: %s\n' % str(exception))
        await context.send(str(exception))

    async def on_command_error(self, context, exception):
        with open('err.log', 'a') as f:
            f.write('Command Exception: %s\n' % str(exception))
        await context.send(str(exception))
