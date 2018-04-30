import re

async def completed(message):
    await message.add_reaction("check:440135593037660180")

def has_emoji(text):
    words = text.split(' ')
    emojis = []
    for word in words:
        emojis.append(is_emoji(word))
    return len(emojis) != 0

def is_emoji(text):
    pattern = r':(A-Za-z0-9)?:'
    return re.search(pattern, text)