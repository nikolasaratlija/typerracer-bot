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
        player = Player(member)
        await lobby.add_player(player)
        await lobby.channel.send(f"{member.mention} has joined lobby the lobby!")

    async def send_text(self, lobby: Lobby):
        lobby.current_text = self.TEXTS[randint(0, len(self.TEXTS) - 1)]
        await lobby.channel.send(lobby.current_text)


def setup(bot):
    bot.add_cog(LobbyManager(bot))

    @commands.command(name="start")
    @is_called_from_lobby(LobbyManager.lobbies)
    @is_lobby_host(LobbyManager.lobbies)
    async def wait_for_host(ctx):
        await ctx.send("Host has started the race!")

    @wait_for_host.error
    async def start_error(ctx, error):
        if isinstance(error, NotCalledFromALobby):
            await ctx.send(f"{ctx.message.author.mention}, this channel is not a Typeracer lobby.")

        if isinstance(error, NotAHost):
            await ctx.send(f"{ctx.message.author.mention}, you are not the host of this lobby.")

    @commands.command()
    @is_not_called_from_lobby(LobbyManager.lobbies)
    @user_not_in_lobby(LobbyManager.lobbies)
    # @lobby_exists(LobbyManager.lobbies)
    async def join(ctx, lobby_id):
        try:
            lobby = next(lobby for lobby in LobbyManager.lobbies if lobby.lobby_id == lobby_id)
            await LobbyManager.add_player(lobby, ctx.message.author)
        except StopIteration:
            raise LobbyNotFound

    @join.error
    async def join_error(ctx, error):
        if isinstance(error, DuplicatePlayer):
            await ctx.send(f"{ctx.message.author.mention}, you're already in a lobby.")

        if isinstance(error, LobbyNotFound):
            await ctx.send(f"{ctx.message.author.mention}, the channel you're trying to join does not exist.")

    bot.add_command(wait_for_host)
    bot.add_command(join)
