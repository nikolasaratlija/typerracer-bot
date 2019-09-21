from discord import TextChannel
from typing import List


class Utils:
    @staticmethod
    def find_lobby_by_id(channel_id: int, channel_list: List[TextChannel]):
        return next(
            channel for channel in channel_list
            if next(int(s) for s in channel.name.split() if s.isdigit()) == channel_id)
