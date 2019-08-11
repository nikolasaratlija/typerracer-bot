import discord
from discord.ext import commands

from .helper import Helper
from .lobby_creator import LobbyCreator
from .lobby_manager import LobbyManager
from .lobby_referee import LobbyReferee

typeracer = commands.Bot(command_prefix='$typeracer ')

typeracer.remove_command("help")  # removes the built-in help command

typeracer.add_cog(Helper(typeracer))

typeracer.add_cog(LobbyCreator(typeracer))
typeracer.add_cog(LobbyManager(typeracer))
typeracer.add_cog(LobbyReferee(typeracer))


@typeracer.event
async def on_ready():
    await typeracer.change_presence(
        activity=discord.Game(str(typeracer.command_prefix) + "help"))
