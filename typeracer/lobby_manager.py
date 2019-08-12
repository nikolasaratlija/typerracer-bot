from typing import List
from random import randint
from json import load

from .lobby import Lobby
from .player import Player
from .exceptions import *

from discord.ext import commands


class LobbyManager(commands.Cog):
    lobbies: List[Lobby] = []

    def __init__(self, bot):
        self.bot = bot
        with open("texts.json") as json_file:
            self.TEXTS = load(json_file)['texts']

    def manage(self, lobby: Lobby):
        self.lobbies.append(lobby)

    @commands.command()
    async def join(self, ctx, lobby_id):
        # checks if the lobby the member is trying to join exists
        try:
            # tries to the find the lobby by its id
            lobby = next(lobby for lobby in self.lobbies if lobby.lobby_id == lobby_id)
            await self.add_player(lobby, ctx.message.author)
        except StopIteration:
            await ctx.send("A lobby with id " + lobby_id + " does not exist.")

    @join.error
    async def join_error(self, ctx, error):
        if isinstance(error, DuplicatePlayer):
            await ctx.send(f"{ctx.message.author.mention}, you're already in a lobby.")

    @staticmethod
    async def add_player(lobby: Lobby, player: Player):
        await lobby.add_player(player)
        await lobby.channel.send(f"{player.member.mention} has joined lobby the lobby!")

    async def send_text(self, lobby: Lobby):
        lobby.current_text = self.TEXTS[randint(0, len(self.TEXTS) - 1)]
        await lobby.channel.send(lobby.current_text)


def setup(bot):
    bot.add_cog(LobbyManager(bot))

    @commands.command(name="start")
    @is_called_from_lobby(LobbyManager.lobbies)
    @is_lobby_host(LobbyManager.lobbies)
    async def wait_for_host(ctx):
        print(1)
        await ctx.send("Host has started the race!")

    @wait_for_host.error
    async def start_error(ctx, error):
        if isinstance(error, NotCalledFromALobby):
            await ctx.send(f"{ctx.message.author.mention}, this channel is not a Typeracer lobby.")

        if isinstance(error, NotAHost):
            await ctx.send(f"{ctx.message.author.mention}, you are not the host of this lobby.")

    bot.add_command(wait_for_host)
