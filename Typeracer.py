import discord
from random import randint
from typing import List
from dotenv import load_dotenv
from os import getenv

load_dotenv()
TOKEN = getenv("DISCORD_BOT_TOKEN")

texts = [
    "You are what you are and you are where you are because of what has gone into your mind. You change what you are and you change where you are by changing what goes into your mind.",
    "What you don't have you don't need it now. What you don't know you can feel it somehow. What you don't have you don't need it now.",
    "When I need to find something out, I just go out and look for somebody that knows more than me, and I go and ask them. Sometimes I ask pretty hard.",
    "You are what you are and you are where you are because of what has gone into your mind. You change what you are and you change where you are by changing what goes into your mind.",
    "For what you see and hear depends a good deal on where you are standing. It also depends on what sort of person you are."
]


class Typeracer(discord.Client):
    participants: List[discord.Member] = []
    race_text: str = ""
    is_ongoing_race: bool = False

    async def on_message(self, message):
        # ignores the messages by the bot itself
        if message.author == self.user:
            return

        # can start a race by typing a certain command
        if message.content == '/typeracer start':
            if self.is_ongoing_race is True:
                return await message.channel.send("A race has already been started.")

            await self.announce_race(message)
            await self.send_random_text(message)

        if self.is_ongoing_race:
            # adds members of the server to the race
            if message.content == "/typeracer join":
                await message.channel.send("<@" + str(message.author.id) + ">" + " has joined the race!")
                self.participants.append(message.author)

            # members who type out the text correctly, win
            if message.author in self.participants and message.content == self.race_text:
                # messages the winners
                await message.channel.send("<@" + str(message.author.id) + ">" + " got it right!")
                self.race_text = ""

    async def announce_race(self, message: discord.Message):
        self.is_ongoing_race = True
        await message.channel.send("A new race has started! You have 5 seconds to type `/join race` to participate.")

    async def send_random_text(self, message: discord.Message):
        # picks a random text and messages it to the server
        self.race_text = texts[randint(0, len(texts) - 1)]
        await message.channel.send(self.race_text)


client = Typeracer()
client.run(TOKEN)
