from discord import TextChannel
from typing import List
from .player import Player


class Lobby:
    players: List[Player] = []
    is_started: bool = False
    current_text: str = ""

    def __init__(self, lobby_id, channel: TextChannel):
        self.lobby_id = lobby_id
        self.channel = channel

    def add_player(self, player: Player):
        self.players.append(player)
