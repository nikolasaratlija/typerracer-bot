from discord.ext import commands
from random import randint

from .party import Party
from .party_manager import PartyManager


class PartyGenerator(commands.Cog):
    """"Creates a dedicated channel in which a typing race will be held"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="create-party")
    async def create_party(self, ctx):
        # tries to find a channel category named "typeracers races". If it can't find one, it gets created
        try:
            races_category = next(category for category in ctx.guild.categories if category.name == "typeracer races")
        except StopIteration:
            races_category = await ctx.guild.create_category("typeracer races")

        # unique_key is used for identifying a party channel
        unique_key = str(hex(randint(0, 255))[2:])  # a random hexadecimal number between 0 and 255
        party = await races_category.create_text_channel("Typeracer party " + str(unique_key))

        await ctx.send("Typeracer party " + str(unique_key) + " created.")

        manager: PartyManager = self.bot.get_cog('PartyManager')
        await manager.prepare(Party(unique_key, party), ctx)
