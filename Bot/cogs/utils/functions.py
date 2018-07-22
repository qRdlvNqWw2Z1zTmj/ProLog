class Functions:

    async def completed(self, message):
        await message.add_reaction(":check:444926155800444949")

    async def not_completed(self, message):
        await message.add_reaction("negative:444926170895613962")

    def escape(self, cont):
        for c in cont:
            cont.replace(c, f'\{c}')
        return cont
