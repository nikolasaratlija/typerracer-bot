from discord.ext import commands
from random import randint
from Typeracer import Party


class PartyGenerator(commands.Cog):
    """"Creates a dedicated channel in which a typing race will be held"""

    @commands.command()
    async def create_party(self, ctx):
        # tries to find a channel category named "typeracers races". If it can't find one, it gets created
        try:
            races_category = next(category for category in ctx.guild.categories if category.name == "typeracer races")
        except StopIteration:
            races_category = await ctx.guild.create_category("typeracer races")

        unique_key = str(hex(randint(0, 255))[2:])  # a random hexadecimal number between 0 and 255
        party = await races_category.create_text_channel("🏁 Typeracer party - #" + str(unique_key))

        # returns a unique key used for identifying the newly created channel
        return Party.Party(unique_key, party)
