from typing import List
from random import randint
from json import load

from .lobby import Lobby
from .player import Player
from .checks import *

from discord.ext import commands
from discord import Member


class LobbyManager(commands.Cog):
    lobbies: List[Lobby] = []

    def __init__(self, bot):
        self.bot = bot
        with open("texts.json") as json_file:
            self.TEXTS = load(json_file)['texts']

    def manage(self, lobby: Lobby):
        self.lobbies.append(lobby)

    @staticmethod
    async def add_player(lobby: Lobby, member: Member):
        await lobby.add_player(member)
        await lobby.channel.send(f"{member.mention} has joined lobby the lobby!")

    def send_text(self):
        return self.TEXTS[randint(0, len(self.TEXTS) - 1)]


def setup(bot):
    bot.add_cog(LobbyManager(bot))
    lobby_manager = bot.get_cog('LobbyManager')

    @commands.command()
    @is_called_from_lobby(lobby_manager.lobbies)
    @is_lobby_host(lobby_manager.lobbies)
    async def start(ctx):
        await ctx.send("Host has started the race!")
        await ctx.send(lobby_manager.send_text())

    @start.error
    async def start_error(ctx, error):
        if isinstance(error, NotCalledFromALobby):
            await ctx.send(f"{ctx.message.author.mention}, this channel is not a Typeracer lobby.")

        if isinstance(error, NotAHost):
            await ctx.send(f"{ctx.message.author.mention}, you are not the host of this lobby.")

    @commands.command()
    @is_not_called_from_lobby(lobby_manager.lobbies)
    @user_not_in_lobby(lobby_manager.lobbies)
    # @lobby_exists(LobbyManager.lobbies)
    async def join(ctx, lobby_id):
        try:
            lobby = next(lobby for lobby in lobby_manager.lobbies if lobby.lobby_id == lobby_id)
            await lobby_manager.add_player(lobby, ctx.message.author)
        except StopIteration:
            raise LobbyNotFound

    @join.error
    async def join_error(ctx, error):
        if isinstance(error, DuplicatePlayer):
            await ctx.send(f"{ctx.message.author.mention}, you're already in a lobby.")

        if isinstance(error, LobbyNotFound):
            await ctx.send(f"{ctx.message.author.mention}, the channel you're trying to join does not exist.")

    bot.add_command(start)
    bot.add_command(join)
