import discord
from typing import Dict


class Typeracer(discord.Client):
    __JOINING_PHASE_TIMER: int = 10

    players: Dict[discord.Member, Dict] = {}
    current_text: str = ""
    is_joining_phase: bool = False
    race_is_ongoing: bool = False

    async def on_ready(self):
        await self.change_presence(activity=discord.Game("/typeracer help"))

    async def on_message(self, message):
        # region messages by the bot itself are ignored
        if message.author == self.user:
            return
        # endregion

        # region command join: adds members of the server to the race
        if message.content == "/typeracer join" and self.is_joining_phase is True:
            await message.channel.send(str(message.author.mention) + " has joined the race!")
            self.players[message.author] = {"finished": False}
        # endregion

        # region members who type out the text correctly during a race, win
        if self.race_is_ongoing is True:
            if message.author in self.players and message.content == self.current_text:
                await self.mention_finishers(message.channel, message.author)
            # checks whether all players have finished
            if all(player["finished"] is True for player in self.players.values()) is True:
                await self.close_race("All players have finished!", message.channel)
        # endregion
