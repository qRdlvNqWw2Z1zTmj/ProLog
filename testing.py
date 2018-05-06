from bot import ProLog
import config
import traceback
import sys

if __name__ == '__main__':
    bot = ProLog(command_prefix=None)
    bot.run(config.testingtoken)
