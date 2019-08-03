import discord
from random import randint
from typing import Dict
from asyncio import sleep
from Typeracer import anti_copy


TEXTS = [
    "You are what you are and you are where you are because of what has gone into your mind. You change what you are and you change where you are by changing what goes into your mind.",
    "What you don't have you don't need it now. What you don't know you can feel it somehow. What you don't have you don't need it now.",
    "When I need to find something out, I just go out and look for somebody that knows more than me, and I go and ask them. Sometimes I ask pretty hard.",
    "You are what you are and you are where you are because of what has gone into your mind. You change what you are and you change where you are by changing what goes into your mind.",
    "For what you see and hear depends a good deal on where you are standing. It also depends on what sort of person you are."
]


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

        # region command help: prints a list of commands
        if message.content == '/typeracer help':
            await message.channel.send(
                "A bot inspired by typeracer.com, made by <@106574735713767424> \n"
                "Command list: \n"
                "`/typeracer help`: A list of commands. \n"
                "`/typeracer start`: Starts a new race. Client will be given 10 seconds to join the race. \n"
                "`/typeracer join`: Adds the client who typed this command to a race if one has been started.")
        # endregion

        # region command start: can start a race by typing a certain command
        if message.content == '/typeracer start' and self.is_joining_phase is False:
            await self.announce_race(message.channel)
            await sleep(self.__JOINING_PHASE_TIMER)  # this waiting period gives clients time to join the race

            # stops if no one joins the race
            if len(self.players) == 0:
                return await self.close_race("No one joined the race...", message.channel)

            await self.countdown(message.channel)
            await self.send_random_text(message.channel)
        # endregion

        # region command join: adds members of the server to the race
        if message.content == "/typeracer join" and self.is_joining_phase is True:
            await message.channel.send("<@" + str(message.author.id) + ">" + " has joined the race!")
            self.players[message.author] = {"finished": False}
        # endregion

        # region members who type out the text correctly during a race, win
        if self.race_is_ongoing is True:
            if message.author in self.players and message.content == self.current_text:
                await self.mention_finishers(message.author, message.channel)
            # checks whether all players have finished
            if all(player["finished"] is True for player in self.players.values()) is True:
                await self.close_race("All players have finished!", message.channel)
        # endregion

    async def close_race(self, reason: str, channel: discord.TextChannel):
        self.is_joining_phase = False
        self.race_is_ongoing = False
        await channel.send(reason + " To start a new race, type `/typeracer start`.")

    async def mention_finishers(self, winner: discord.Member, channel: discord.TextChannel):
        self.players[winner]["finished"] = True
        await channel.send(winner.mention + " got it right!")

    async def announce_race(self, channel: discord.TextChannel):
        self.is_joining_phase = True
        await channel.send(
            "A new race has started! "
            "You have " + str(self.__JOINING_PHASE_TIMER) + " seconds to type `/typeracer join` to participate.")

    async def send_random_text(self, channel: discord.TextChannel):
        self.current_text = TEXTS[randint(0, len(TEXTS) - 1)]
        await channel.send(
            anti_copy.encrypt(self.current_text))

    async def countdown(self, channel: discord.TextChannel):
        self.is_joining_phase = False
        await channel.send("All participants have been locked in.")
        await sleep(1)
        await channel.send("Ready.")
        await sleep(1)
        await channel.send("Set.")
        await sleep(randint(1, 3))  # This interval is random because I thought it would be funny.
        await channel.send("Type!")
        self.race_is_ongoing = True
