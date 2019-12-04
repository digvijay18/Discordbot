"""
This file contains the WebCommands class. This class contains all the commands
that will be available on the bot once loaded onto the bot. To add a new command,
add a new function with the name "command_<commmand value>" and restart the bot.
The <command value> keyword will be available for use for the chat client.
"""

from discord.ext.commands import Command

from app import store
from app import constants


class WebCommands(object):
    @classmethod
    def list_commands(cls):
        """
        This is a class method that is used to collect all bot commands,
        instantiate it as a Command class object and return the list of
        Command objects to the Bot class object for registration.
        """
        for func in dir(cls):
            if callable(getattr(cls, func)) and func.startswith('command_'):
                command = Command(getattr(cls, func), name=func.split('_')[1])
                yield command

    @staticmethod
    async def command_google(sender, keywords):
        """
        This is the command function that responds to !google message from
        client.
        """
        keywords = keywords.replace('_', ' ')
        _store = store.Store(use_cache=True)
        result = _store.search(keywords, constants.RESULT)
        await sender.send(result)

    @staticmethod
    async def command_recent(sender, keywords):
        """
        This is the command function that responds to !recent message from
        client.
        """
        keywords = keywords.replace('_', ' ')
        _store = store.Store(use_cache=True)
        result = _store.search(keywords, constants.HISTORY)
        await sender.send(result)
