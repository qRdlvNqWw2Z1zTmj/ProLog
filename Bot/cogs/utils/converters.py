from discord.ext import commands

from ..utils import data


class ModuleConverter(commands.Converter):
    async def convert(self, ctx, argument):
        try:
            category = argument[: argument.index("-")]
            module = argument[argument.index("-") + 1 :]
        except ValueError:
            await ctx.send(f"'{argument}' is not a valid module category or module")
            return

        catvalid = False
        modvalid = False
        for mck, mcv in data.modules.items():
            # Check category and fix cases
            if category.lower() == str(mck).lower():
                category = str(mck)
                catvalid = True
            else:
                continue

            # Check module and fix cases
            for m in list(mcv):
                if module.lower() == m.lower():
                    module = m
                    modvalid = True
                else:
                    continue

        if not catvalid or not modvalid:
            await ctx.send(f"Module category or module is not valid.")

        return category, module
