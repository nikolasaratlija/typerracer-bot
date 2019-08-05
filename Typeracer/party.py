from discord import TextChannel
from typing import List
from Typeracer import player


class Party:
    players: List[player.Player] = []
    is_started: bool = False
    current_text: str = ""

    def __init__(self, party_id, channel: TextChannel):
        self.party_id = party_id
        self.channel = channel

    def add_player(self, player: player):
        self.players.append(player)
