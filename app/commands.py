from discord.ext.commands import Command

import store
import constants


class WebCommands(object):
    def __init__(self):
        self.store = store.Store(use_cache=True)

    def list_commands(self):
        for func in dir(self):
            if callable(getattr(self, func)) and func.startswith('command_'):
                command = Command(getattr(self, func), name=func.split('_')[1])
                yield command

    async def command_google(self, sender, keywords):
        keywords = keywords.replace('_', ' ')
        result = self.store.search(keywords, constants.RESULT)
        await sender.send(result)

    async def command_recent(self, sender, keywords):
        keywords = keywords.replace('_', ' ')
        result = self.store.search(keywords, constants.HISTORY)
        await sender.send(result)
