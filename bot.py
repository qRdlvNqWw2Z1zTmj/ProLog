import sys
import traceback

import discord
from discord.ext import commands

import config


class ProLog(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        print('=' * 10)
        print(f'Logged in as {self.user} with the id {self.user.id}')
        print(f"Loaded {cogs[:-2]}")
        print(f'Guild count: {len(self.guilds)}')
        print('=' * 10)

    async def on_message(self, message):
        if not isinstance(message.channel, discord.TextChannel):
            return
        if message.author.bot:
            return
        await self.process_commands(message)

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Required argument `{error.param.name}` is missing. See {bot.command_prefix[0]}help {ctx.command.name}")




if __name__ == '__main__':
    # Def bot
    bot = ProLog(command_prefix=['?', "!"])
    bot.remove_command("help")



    # Load cogs
    cogs = ""
    for extension in ["cogs.help", "cogs.dev", "cogs.eval", "cogs.general", "cogs.temp"]:
        try:
            bot.load_extension(extension)
            cogs += f"{extension[extension.index('.') + 1:]}, "
        except Exception as e:
            print(f'Failed to load extension {extension}.', file=sys.stderr)
            traceback.print_exc()

    # Run bot
    bot.run(config.token)