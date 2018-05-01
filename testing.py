from bot import ProLog
from bot import EXTENSIONS
import config
import traceback
import sys

if __name__ == '__main__':
    # Def bot
    bot = ProLog(command_prefix=ProLog.prefix)

    # Load cogs
    for extension in EXTENSIONS:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f'Failed to load extension {extension}.', file=sys.stderr)
            traceback.print_exc()

    # Run bot
    try:
        bot.run(config.testingtoken)
    finally:
        pass