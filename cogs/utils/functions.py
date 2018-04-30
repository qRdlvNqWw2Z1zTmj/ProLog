import re
from discord.ext.commands import EmojiConverter

async def completed(message):
    await message.add_reaction("check:440135593037660180")

async def has_emoji(ctx, text):
    words = text.split(' ')
    emojis = []
    for word in words:
        emojis.append(await is_emoji(ctx, word))
    return len(emojis) != 0

async def is_emoji(ctx, text):
    return await EmojiConverter().convert(ctx, text)