import discord
from discord.ext import commands

from .helper import Helper
from .party_generator import PartyGenerator
from .party_manager import PartyManager

typeracer = commands.Bot(command_prefix='$typeracer ')

typeracer.remove_command("help")  # removes the built-in help command

typeracer.add_cog(Helper(typeracer))
typeracer.add_cog(PartyGenerator(typeracer))
typeracer.add_cog(PartyManager(typeracer))


@typeracer.event
async def on_ready():
    await typeracer.change_presence(
        activity=discord.Game(str(typeracer.command_prefix) + " help"))
