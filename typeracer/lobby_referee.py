from typing import List

from discord import Member
from discord.ext import commands

from .lobby import Lobby


class LobbyReferee(commands.Cog):
    """Keeps track of players in a race; what they type, when they win, WPM, etc."""

    watched_lobbies: List[Lobby] = []

    def __init__(self, bot):
        self.bot = bot

    def watch(self, lobby: Lobby):
        self.watched_lobbies.append(lobby)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        # makes sure to only read messages from discord channels that are being watched by this class
        try:
            lobby = next(lobby for lobby in self.watched_lobbies if lobby.channel.id == message.channel.id)
        except StopIteration:
            return

        if message.content == lobby.current_text:
            await self.notify_finisher(lobby, message.author)

    @staticmethod
    async def notify_finisher(lobby: Lobby, winner: Member):
        await lobby.channel.send(f"{winner.mention} got it right!")
