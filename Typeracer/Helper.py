from discord.ext import commands


class Helper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def commands(self, ctx):
        prefix = str(self.bot.command_prefix)

        await ctx.send(
            "Command list: \n"
            "`" + prefix + "commands`: A list of commands. \n"
            "`" + prefix + "create-party`: Starts a new race. Client will be given 10 seconds to join the race. \n"
            "`" + prefix + "join`: Adds the client who typed this command to a race if one has been started.")
