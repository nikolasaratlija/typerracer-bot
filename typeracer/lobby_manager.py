from discord.ext import commands

from typing import List
from random import randint
from json import load

from .entities.lobby import Lobby
import typeracer.exceptions as exceptions
import typeracer.checks as checks


class LobbyManager(commands.Cog):
    lobbies: List[Lobby] = []

    def __init__(self, bot):
        self.bot = bot
        with open("texts.json") as json_file:
            self.TEXTS = load(json_file)['texts']

    def manage(self, lobby: Lobby):
        self.lobbies.append(lobby)

    def get_random_text(self):
        return self.TEXTS[randint(0, len(self.TEXTS) - 1)]


def setup(bot):
    bot.add_cog(LobbyManager(bot))
    lobby_manager = bot.get_cog('LobbyManager')

    @commands.command()
    @checks.is_called_from_lobby(lobby_manager.lobbies)
    @checks.is_lobby_host(lobby_manager.lobbies)
    async def start(ctx):
        await ctx.send("Host has started the race!")
        await ctx.send(lobby_manager.get_random_text())

    @start.error
    async def start_error(ctx, error):
        if isinstance(error, exceptions.NotCalledFromLobby):
            await ctx.send(f"{ctx.message.author.mention}, this channel is not a Typeracer lobby.")

        if isinstance(error, exceptions.NotLobbyHost):
            await ctx.send(f"{ctx.message.author.mention}, you are not the host of this lobby.")

    @commands.command()
    @checks.lobby_exists(lobby_manager.lobbies)
    @checks.is_not_called_from_lobby(lobby_manager.lobbies)
    @checks.user_not_in_lobby(lobby_manager.lobbies)
    async def join(ctx, lobby_id):
        lobby = Lobby.get_lobby_by_id(lobby_id, lobby_manager.lobbies)
        await lobby.add_player(ctx.message.author)

    @join.error
    async def join_error(ctx, error):
        if isinstance(error, exceptions.DuplicatePlayer):
            await ctx.send(f"{ctx.message.author.mention}, you're already in a lobby.")

        if isinstance(error, exceptions.LobbyNotFound):
            await ctx.send(f"{ctx.message.author.mention}, the channel you're trying to join does not exist.")

        if isinstance(error, exceptions.CalledFromALobby):
            await ctx.send(f"{ctx.message.author.mention}, you can't use this command in this channel.")

    bot.add_command(start)
    bot.add_command(join)
