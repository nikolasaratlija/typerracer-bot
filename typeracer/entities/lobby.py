from discord import TextChannel, Member
from typing import List
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

    async def set_host(self, host: Member):
        self.host = host
        await self.add_player(host)
        await self.channel.send(f"{self.host.mention} is the host of this lobby.")

    @staticmethod
    def find_lobby_by_id(channel_id: int, channel_list: List[TextChannel]):
        return next(
            channel for channel in channel_list
            if next(int(string) for string in channel.name.split() if string.isdigit()) == channel_id)
