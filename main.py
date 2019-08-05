from os import getenv

from dotenv import load_dotenv
from discord.ext import commands

from Typeracer import Helper
from Typeracer import PartyGenerator
from Typeracer import PartyManager

load_dotenv()
TOKEN = getenv("DISCORD_BOT_TOKEN")

typeracer = commands.Bot(command_prefix='$typeracer ')

typeracer.add_cog(Helper(typeracer))
typeracer.add_cog(PartyGenerator(typeracer))
typeracer.add_cog(PartyManager(typeracer))

typeracer.run(TOKEN)
