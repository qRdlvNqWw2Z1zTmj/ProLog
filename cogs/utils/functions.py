async def completed(message):
    await message.add_reaction(":check:444926155800444949")

async def not_completed(message):
    await message.add_reaction("negative:444926170895613962")

def escape(cont):
    cont = cont.replace('*', '\*')
    cont = cont.replace('__', '\_\_')
    cont = cont.replace('`', '\`')
    cont = cont.replace('~~', '\~\~')
    return cont