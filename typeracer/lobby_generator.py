from discord import CategoryChannel
from discord.ext import commands
from random import randint

from .lobby import Lobby
from .lobby_manager import LobbyManager


class LobbyGenerator(commands.Cog):
    """"Creates a dedicated channel in which a typing race will be held"""

    __CATEGORY_NAME = "typeracer lobbies"

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="create-lobby")
    async def create_lobby(self, ctx):
        # tries to find a channel category named "typeracer lobbies". If it can't find one, it gets created
        try:
            category = next(category for category in ctx.guild.categories if category.name == self.__CATEGORY_NAME)
        except StopIteration:
            category = await self.create_category(ctx)

        # unique_key is used for identifying a lobby channel
        unique_key = str(hex(randint(0, 255))[2:])  # a random hexadecimal number between 0 and 255
        lobby = await category.create_text_channel("typeracer lobby " + str(unique_key))

        await ctx.send(
            f"{lobby.mention} has been created! "
            f"Type `{self.bot.command_prefix}join {str(unique_key)}` to join the lobby.")

        typeracer_lobby = Lobby(unique_key, lobby, ctx.message.author)

        manager: LobbyManager = self.bot.get_cog('LobbyManager')
        await manager.prepare(typeracer_lobby, ctx)

    async def create_category(self, ctx):
        category: CategoryChannel = await ctx.guild.create_category(self.__CATEGORY_NAME)
        # finds the `everyone` discord role
        role_everyone = next(role for role in ctx.guild.roles if role.name == "@everyone")
        # restricts permissions for every channel under the "typeracer lobbies" category
        await category.set_permissions(target=role_everyone, read_messages=False)
        await category.set_permissions(target=self.bot.user, read_messages=True)
        return category
