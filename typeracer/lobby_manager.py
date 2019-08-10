from typing import List
from asyncio import sleep
from random import randint
import json

import discord
from discord.ext import commands

from .exceptions import NoParticipantsException
from .lobby import Lobby
from .lobby_referee import LobbyReferee


class LobbyManager(commands.Cog):
    __JOINING_PHASE_TIMER = 10

    lobbies: List[Lobby] = []

    def __init__(self, bot):
        self.bot = bot
        with open("texts.json") as json_file:
            self.TEXTS = json.load(json_file)['texts']

    async def prepare(self, lobby: Lobby, ctx):
        self.lobbies.append(lobby)
        try:
            await self.await_players(lobby, ctx.message.channel)
            await self.countdown(lobby)
            await self.send_text(lobby)
            referee: LobbyReferee = self.bot.get_cog("LobbyReferee")
            referee.watch(lobby)
        except NoParticipantsException:
            await lobby.channel.send("No one joined the lobby...")

    @commands.command()
    async def join(self, ctx, lobby_id):
        # checks if the lobby the member is trying to join exists
        if self.lobbies:
            try:
                lobby = next(lobby for lobby in self.lobbies if lobby.lobby_id == lobby_id)
                lobby.add_player(ctx.message.author)
                await lobby.channel.send(ctx.message.author.mention + " has joined lobby " + lobby_id)
            except StopIteration:
                await ctx.send("A lobby with id " + lobby_id + " does not exist.")

    async def await_players(self, lobby: Lobby, called_from: discord.TextChannel):
        def countdown_message_generator(sec):
            return "A new race has started! You have " + str(sec) + \
                   " second(s) to type `" + str(self.bot.command_prefix) + "join " + lobby.lobby_id + "` to join."

        countdown_message = await called_from.send(
            countdown_message_generator(self.__JOINING_PHASE_TIMER))

        # counts down the number in `countdown_message` by editing it in a loop
        for seconds in range(self.__JOINING_PHASE_TIMER):
            await discord.Message.edit(
                countdown_message,
                content=countdown_message_generator(self.__JOINING_PHASE_TIMER - seconds))
            await sleep(1)

        await discord.Message.edit(countdown_message, content="Invite for lobby " + lobby.lobby_id + " expired.")

        # if no one joins a race, raise an exception
        if not lobby.players:
            raise NoParticipantsException

    @staticmethod
    async def countdown(lobby: Lobby):
        message = await lobby.channel.send("All participants have been locked in...")
        await sleep(1)
        await discord.Message.edit(message, content="Ready?")
        await sleep(1)
        await discord.Message.edit(message, content="Set.")
        await sleep(randint(1, 3))  # This interval is random because I thought it would be funny.
        await discord.Message.edit(message, content="Type!")

    async def send_text(self, lobby: Lobby):
        lobby.current_text = self.TEXTS[randint(0, len(self.TEXTS) - 1)]
        await lobby.channel.send(lobby.current_text)

    async def close_lobby(self, lobby: Lobby):
        # announce that channel will be closing upon all players finishing the race or timeout
        print("lobby: '" + lobby.lobby_id + "' closed.")
