import discord
from discord.ext import commands

from Typeracer import Helper
from Typeracer import PartyGenerator
from Typeracer import PartyManager

typeracer = commands.Bot(command_prefix='$typeracer ')

typeracer.remove_command("help")

typeracer.add_cog(Helper.Helper(typeracer))
typeracer.add_cog(PartyGenerator.PartyGenerator(typeracer))
typeracer.add_cog(PartyManager.PartyManager(typeracer))


@typeracer.event
async def on_ready():
    await typeracer.change_presence(
        activity=discord.Game(str(typeracer.command_prefix) + " help"))
