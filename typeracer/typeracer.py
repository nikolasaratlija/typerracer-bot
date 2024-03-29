import discord
from discord.ext import commands

from .helper import Helper
from .lobby_creator import LobbyCreator
from .lobby_referee import LobbyReferee

typeracer = commands.Bot(command_prefix='$typeracer ')

typeracer.remove_command("help")  # removes the built-in help command

typeracer.add_cog(Helper(typeracer))

typeracer.add_cog(LobbyCreator(typeracer))
typeracer.load_extension('typeracer.lobby_manager')


@typeracer.event
async def on_ready():
    await typeracer.change_presence(
        activity=discord.Game(str(typeracer.command_prefix) + "help"))
