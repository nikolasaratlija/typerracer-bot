from discord import CategoryChannel, TextChannel
from discord.ext import commands
from random import randint

from .lobby import Lobby
from .lobby_manager import LobbyManager


class LobbyCreator(commands.Cog):
    """Creates channels in which typeracer will be held"""

    __CATEGORY_NAME = "typeracer lobbies"

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="create-lobby")
    async def create_lobby(self, ctx):
        category = await self.get_typeracer_category(ctx)

        # unique_key is used for identifying a lobby channel
        unique_key = str(hex(randint(0, 255))[2:])  # a random hexadecimal number between 0 and 255
        lobby = await category.create_text_channel("typeracer lobby " + str(unique_key))

        typeracer_lobby = Lobby(unique_key, lobby)
        await typeracer_lobby.set_host(ctx.message.author)

        await self.notify_users(typeracer_lobby, ctx)
        await self.delegate_to_manager(typeracer_lobby)

    async def get_typeracer_category(self, ctx):
        """tries to find a channel category named "typeracer lobbies". If it can't find one, it gets created"""
        try:
            return next(category for category in ctx.guild.categories if category.name == self.__CATEGORY_NAME)
        except StopIteration:
            return await self.create_category(ctx)

    async def create_category(self, ctx):
        category: CategoryChannel = await ctx.guild.create_category(self.__CATEGORY_NAME)
        # finds the `everyone` discord role
        role_everyone = next(role for role in ctx.guild.roles if role.name == "@everyone")
        # restricts permissions for every channel under the "typeracer lobbies" category
        await category.set_permissions(target=role_everyone, read_messages=False)
        await category.set_permissions(target=self.bot.user, read_messages=True)
        return category

    async def notify_users(self, lobby: Lobby, channel: TextChannel):
        await channel.send(
            f"{lobby.channel.mention} has been created! "
            f"Type `{self.bot.command_prefix}join {lobby.lobby_id}` to join the lobby.")

    async def delegate_to_manager(self, lobby: Lobby):
        manager: LobbyManager = self.bot.get_cog('LobbyManager')
        manager.manage(lobby)
