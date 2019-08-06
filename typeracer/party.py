from discord import TextChannel
from typing import List
from .player import Player


class Party:
    players: List[Player] = []
    is_started: bool = False
    current_text: str = ""

    def __init__(self, party_id, channel: TextChannel):
        self.party_id = party_id
        self.channel = channel

    def add_player(self, player: Player):
        self.players.append(player)
