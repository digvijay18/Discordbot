import os
import discord
from discord.ext.commands import Bot


from dotenv import load_dotenv

load_dotenv()

token = os.getenv('DISCORD_TOKEN')
server_name = os.getenv('DISCORD_SERVER_NAME')


class TesterBot(Bot):
    def register_commands(self, command_set):
        _commands = command_set.list_commands()
        for command in _commands:
            self.add_command(command)

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    async def on_error(self, event, *args, **kwargs):
        with open('err.log', 'a') as f:
            if event == 'on_message':
                f.write(f'Unhandled message: {args[0]}\n')
            else:
                raise discord.DiscordException
