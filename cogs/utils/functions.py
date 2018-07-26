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

    async def module_settings_selection_panel(message, selectors, numbered=False):
        desc = ""
        i = 1
        for s in selectors:
            if i == 10:
                desc += ("\U0001f51f" if numbered else s[3]) + f" **-** {s[0]}-{s[1]}\n"
                break
            desc += (f"{i}\u20e3" if numbered else s[3]) + f" **-** {s[0]}-{s[1]}\n"
            i += 1

        embed = await message.channel.send(
            embed=discord.Embed(title='Selections:' if len(selectors) > 1 else 'Selection:', description=desc, color=discord.Color.dark_teal()))
        i = 1
        for s in selectors:
            await embed.add_reaction(f"{i}\u20e3" if i < 10 else "\U0001f51f")
            i += 1
