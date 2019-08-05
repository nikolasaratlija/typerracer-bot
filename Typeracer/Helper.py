from discord.ext import commands


class Helper(commands.Cog):
    @commands.command()
    async def commands(self, ctx):
        await ctx.send(
            "Command list: \n"
            "`/typeracer help`: A list of commands. \n"
            "`/typeracer start`: Starts a new race. Client will be given 10 seconds to join the race. \n"
            "`/typeracer join`: Adds the client who typed this command to a race if one has been started.")
