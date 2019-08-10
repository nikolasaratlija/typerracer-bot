from discord.ext import commands


class Helper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        prefix = str(self.bot.command_prefix)

        await ctx.send(
            "__**Commands**__: \n"
            f"**{prefix}help**: A list of commands. \n"
            f"**{prefix}create-lobby**: Creates a new channel in which the race will be held. \n"
            f"**{prefix}join (lobby id)**: Adds you to a lobby, provided the given ID is correct.")
