# 1 more
import sys
import traceback
import json

import discord
from discord.ext import commands

import config


class ProLog(commands.Bot):
    def __init__(self, *args, **kwargs):
        try:
            self.pref_file = open('prefixes.json', 'r')
        except FileNotFoundError:
            with open('prefixes.json', 'w') as f:
                json.dump({}, f)
            self.pref_file = open('prefixes.json', 'r')
        self.prefixes = json.load(self.pref_file)
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
    bot.run(config.token)