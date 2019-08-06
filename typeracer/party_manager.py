from typing import List
from asyncio import sleep
from random import randint
import json

import discord
from discord.ext import commands

from .exceptions import NoParticipantsException
from .party import Party


class PartyManager(commands.Cog):
    __JOINING_PHASE_TIMER = 10

    parties: List[Party] = []

    def __init__(self, bot):
        self.bot = bot
        with open("texts.json") as json_file:
            self.TEXTS = json.load(json_file)['texts']

    async def prepare(self, party: Party, ctx):
        self.parties.append(party)
        try:
            await self.await_players(party, ctx.message.channel)
            await self.countdown(party)
            await self.send_text(party)
        except NoParticipantsException:
            await party.channel.send("No one joined the party...")

    @commands.command()
    async def join(self, ctx, party_id):
        # checks if the party the member is trying to join exists
        if self.parties:
            try:
                party = next(x for x in self.parties if x.party_id == party_id)
                party.add_player(ctx.message.author)
                await party.channel.send(ctx.message.author.mention + " has joined party " + party_id)
            except StopIteration:
                await ctx.send("A party with id " + party_id + " does not exist.")

    async def await_players(self, party: Party, called_from: discord.TextChannel):
        def countdown_message_generator(sec):
            return "A new race has started! You have " + str(sec) + \
                   " second(s) to type `" + str(self.bot.command_prefix) + "join " + party.party_id + "` to join."

        countdown_message = await called_from.send(
            countdown_message_generator(self.__JOINING_PHASE_TIMER))

        # counts down the number in `countdown_message` by editing it in a loop
        for seconds in range(self.__JOINING_PHASE_TIMER):
            await discord.Message.edit(
                countdown_message,
                content=countdown_message_generator(self.__JOINING_PHASE_TIMER - seconds))
            await sleep(1)

        await discord.Message.edit(countdown_message, content="Invite for party " + party.party_id + " expired.")

        # if no one joins a race, raise an exception
        if not party.players:
            raise NoParticipantsException

    @staticmethod
    async def countdown(party: Party):
        message = await party.channel.send("All participants have been locked in...")
        await sleep(1)
        await discord.Message.edit(message, content="Ready?")
        await sleep(1)
        await discord.Message.edit(message, content="Set.")
        await sleep(randint(1, 3))  # This interval is random because I thought it would be funny.
        await discord.Message.edit(message, content="Type!")

    async def send_text(self, party: Party):
        party.current_text = self.TEXTS[randint(0, len(self.TEXTS) - 1)]
        await party.channel.send(party.current_text)

    async def notify_finishers(self):
        print("winner")

    async def close_party(self, party: Party):
        # announce that channel will be closing upon all players finishing the race or timeout
        print("Party: '" + party.party_id + "' closed.")
