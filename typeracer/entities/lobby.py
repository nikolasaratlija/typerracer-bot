from discord import TextChannel, Member
from typing import List

from typeracer.exceptions import LobbyNotFound
from typeracer.entities.player import Player


class Lobby:
    players: List[Player] = []
    race_is_started: bool = False
    current_text: str = ""
    host: Member

    def __init__(self, lobby_id: int, channel: TextChannel):
        self.lobby_id = lobby_id
        self.channel = channel

    async def add_player(self, member: Member):
        player = Player(member)
        self.players.append(player)
        await self.channel.set_permissions(player.member, read_messages=True, send_messages=True)
        await self.channel.send(f"{member.mention} has joined lobby the lobby!")

    async def set_host(self, host: Member):
        self.host = host
        await self.add_player(host)
        await self.channel.send(f"{self.host.mention} is the host of this lobby.")

    @staticmethod
    def get_lobby_by_channel(channel: TextChannel, lobby_list: List['Lobby']):
        try:
            return next(lobby for lobby in lobby_list if lobby.channel == channel)
        except StopIteration:
            return StopIteration

    @staticmethod
    def get_lobby_by_id(lobby_id: int, lobby_list: List['Lobby']):
        try:
            return next(lobby for lobby in lobby_list if lobby.lobby_id == lobby_id)
        except StopIteration:
            raise LobbyNotFound

    @staticmethod
    def get_id_from_string(string: str):
        """extracts the first number from a string and returns it as a string"""
        return next(int(word) for word in string.split() if word.isdigit())
