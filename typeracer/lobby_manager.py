from typing import List
from asyncio import sleep
from random import randint
import json

import discord
from discord.ext import commands

from .lobby import Lobby
from .player import Player


# region check functions

# These check functions are outside of a class because they would'nt work
def is_typeracer_lobby(ctx):
    return any(lobby for lobby in LobbyManager.lobbies
               if lobby.channel == ctx.channel)

# endregion


class LobbyManager(commands.Cog):
    __TIMOUT = 60

    lobbies: List[Lobby] = []

    def __init__(self, bot):
        self.bot = bot
        with open("texts.json") as json_file:
            self.TEXTS = json.load(json_file)['texts']

    def manage(self, lobby: Lobby):
        self.lobbies.append(lobby)

    @commands.command(name="start")
    @commands.check(is_typeracer_lobby)
    async def wait_for_host(self, ctx):
        print(1)

    @commands.command()
    async def join(self, ctx, lobby_id):
        # checks if the lobby the member is trying to join exists
        try:
            # tries to the find the lobby by its id
            lobby = next(lobby for lobby in self.lobbies if lobby.lobby_id == lobby_id)
            await self.add_player(lobby, ctx.message.author)
        except StopIteration:
            await ctx.send("A lobby with id " + lobby_id + " does not exist.")

    @staticmethod
    async def add_player(lobby: Lobby, player: Player):
        await lobby.add_player(player)
        await lobby.channel.send(f"{player.member.mention} has joined lobby the lobby!")

    async def send_text(self, lobby: Lobby):
        lobby.current_text = self.TEXTS[randint(0, len(self.TEXTS) - 1)]
        await lobby.channel.send(lobby.current_text)
