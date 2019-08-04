import discord
from random import randint
from typing import Dict
from asyncio import sleep
from Typeracer import exceptions
import json

with open("texts.json") as json_file:
    TEXTS = json.load(json_file)['texts']


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
        try:
            if message.content == '/typeracer start' and self.is_joining_phase is False:
                await self.await_players(message.channel)
                await self.countdown(message.channel)
                await self.send_random_text(message.channel)
        except exceptions.NoParticipantsException:
            return await self.close_race("No one joined the race...", message.channel)
        # endregion

        # region command join: adds members of the server to the race
        if message.content == "/typeracer join" and self.is_joining_phase is True:
            await message.channel.send(str(message.author.mention) + " has joined the race!")
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

    async def await_players(self, channel: discord.TextChannel):
        self.is_joining_phase = True

        countdown_message = await channel.send(
            "A new race has started!" +
            str(self.__JOINING_PHASE_TIMER) +
            " second(s) to type `/typeracer join` to participate.")

        # counts down the number in `countdown_message` by editing it in a loop
        for seconds in range(self.__JOINING_PHASE_TIMER):
            await discord.Message.edit(
                countdown_message,
                content="A new race has started! You have " +
                        str(self.__JOINING_PHASE_TIMER - seconds) +
                        " second(s) to type `/typeracer join` to participate.")
            await sleep(1)

        await discord.Message.delete(countdown_message)

        # if no one joins a race, raise an exception
        if not self.players:
            raise exceptions.NoParticipantsException

    async def countdown(self, channel: discord.TextChannel):
        self.is_joining_phase = False
        message = await channel.send("All participants have been locked in...")
        await sleep(1)
        await discord.Message.edit(message, content="Ready?")
        await sleep(1)
        await discord.Message.edit(message, content="Set.")
        await sleep(randint(1, 3))  # This interval is random because I thought it would be funny.
        await discord.Message.edit(message, content="Type!")
        self.race_is_ongoing = True

    async def send_random_text(self, channel: discord.TextChannel):
        self.current_text = TEXTS[randint(0, len(TEXTS) - 1)]
        await channel.send(self.current_text)

    async def mention_finishers(self, winner: discord.Member, channel: discord.TextChannel):
        self.players[winner]["finished"] = True
        await channel.send(winner.mention + " got it right!")

    async def close_race(self, reason: str, channel: discord.TextChannel):
        self.is_joining_phase = False
        self.race_is_ongoing = False
        await channel.send(reason + " To start a new race, type `/typeracer start`.")
