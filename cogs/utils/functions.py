import discord


class Functions:

    async def completed(self, message):
        await message.add_reaction(":check:444926155800444949")

    async def not_completed(self, message):
        await message.add_reaction("negative:444926170895613962")

    def escape(self, cont):
        for c in cont:
            cont.replace(c, f'\{c}')
        return cont

    async def selection_panel(self, ctx, selectors):
        desc = '"\n"'.join([s for s in selectors])
        embed = discord.Embed(title='Selections:' if len(selectors) > 1 else 'Selection:', description=desc,
                              color=discord.Color.dark_teal())

    async def module_settings_selector(self, ):
        pass
