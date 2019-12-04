from discord.ext.commands import Command

from app import store
from app import constants


class WebCommands(object):
    def list_commands(self):
        for func in dir(self):
            if callable(getattr(self, func)) and func.startswith('command_'):
                command = Command(getattr(self, func), name=func.split('_')[1])
                yield command

    @staticmethod
    async def command_google(sender, keywords):
        keywords = keywords.replace('_', ' ')
        _store = store.Store(use_cache=True)
        result = _store.search(keywords, constants.RESULT)
        await sender.send(result)

    @staticmethod
    async def command_recent(sender, keywords):
        keywords = keywords.replace('_', ' ')
        _store = store.Store(use_cache=True)
        result = _store.search(keywords, constants.HISTORY)
        await sender.send(result)
