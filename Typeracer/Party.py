from discord import TextChannel
from typing import List
from Typeracer import Player


class Party:
    players: List[Player.Player] = []
    is_started: bool = False
    current_text: str = ""

    def __init__(self, party_id, channel: TextChannel):
        self.party_id = party_id
        self.channel = channel

    def add_player(self, player: Player):
        self.players.append(player)
