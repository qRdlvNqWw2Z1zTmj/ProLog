async def completed(message):
    await message.add_reaction("check:440135593037660180")

def escape(cont):
    cont = cont.replace('*', '\*')
    cont = cont.replace('__', '\_\_')
    cont = cont.replace('`', '\`')
    cont = cont.replace('~~', '\~\~')
    return cont