# 1 more
import sys
import traceback
import json

import discord
from discord.ext import commands

import config

class Prefixes:
    def __init__(self):
        self.file = open('prefixes.json', 'w')
        try:
            with open('prefixes.json', 'r') as f:
                self._data = json.load(f)
        except json.decoder.JSONDecodeError:
            json.dump({}, self.file)
            self._data = {}
        

    def __getitem__(self, item):
        return self._data[item]

    def __setitem__(self, item, value):
        self._data[item] = value
        self.save()

    def __delitem__(self, item):
        del self._data[item]
        self.save()

    def save(self):
        self.file.seek(0)
        json.dump(self._data, self.file)
    
    def close(self):
        self.file.close()
    

class ProLog(commands.Bot):
    def __init__(self, *args, **kwargs):
        self.prefixes = Prefixes()
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        print('=' * 10)
        print(f'Logged in as {self.user} with the id {self.user.id}')
        print(f"Loaded cogs {', '.join([c for c in self.cogs])}") #Seth, this is the proper way
        print(f'Guild count: {len(self.guilds)}')
        print('=' * 10)

    async def on_message(self, message):
        if not isinstance(message.channel, discord.TextChannel):
            return
        if message.author.bot:
            return
        await self.process_commands(message)
        
    async def prefix(self, message):
        try:
            prefixes = self.prefixes[str(message.guild.id)]
        except KeyError:
            self.prefixes[str(message.guild.id)] = ['!']
            self.prefixes.save()
            prefixes = self.prefixes[str(message.guild.id)]
        return commands.when_mentioned_or(*prefixes)(self, message)


if __name__ == '__main__':
    # Def bot
    bot = ProLog(command_prefix=ProLog.prefix)

    # Load cogs
    for extension in ["cogs.help", "cogs.dev", "cogs.eval", "cogs.general", "cogs.temp", "cogs.errorhandler", "cogs.guildevents"]:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f'Failed to load extension {extension}.', file=sys.stderr)
            traceback.print_exc()

    # Run bot
    try:
        bot.run(config.token)
    finally:
        bot.prefixes.save()
        bot.prefixes.close()