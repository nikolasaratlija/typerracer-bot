from discord.ext import commands
from random import randint

from .lobby import Lobby
from .lobby_manager import LobbyManager


class LobbyGenerator(commands.Cog):
    """"Creates a dedicated channel in which a typing race will be held"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="create-lobby")
    async def create_lobby(self, ctx):
        # tries to find a channel category named "typeracers lobbies". If it can't find one, it gets created
        try:
            category = next(category for category in ctx.guild.categories if category.name == "typeracer lobbies")
        except StopIteration:
            category = await ctx.guild.create_category("typeracer lobbies")

        # unique_key is used for identifying a lobby channel
        unique_key = str(hex(randint(0, 255))[2:])  # a random hexadecimal number between 0 and 255
        lobby = await category.create_text_channel("typeracer lobby " + str(unique_key))

        await ctx.send("typeracer lobby " + str(unique_key) + " created.")

        manager: LobbyManager = self.bot.get_cog('lobbyManager')
        await manager.prepare(Lobby(unique_key, lobby), ctx)
