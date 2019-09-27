from discord.ext import commands

from .entities.lobby import Lobby
import typeracer.exceptions as exceptions


def is_lobby_host(lobbies):
    """Checks whether the caller of this command is a host of a lobby"""

    async def predicate(ctx):
        user = ctx.message.author

        if not any(lobby for lobby in lobbies if user == lobby.host):
            raise exceptions.NotAHost
        return True

    return commands.check(predicate)


def is_called_from_lobby(lobbies):
    """Checks whether the channel this command is being called from is a lobby"""

    async def predicate(ctx):
        if not any(lobby for lobby in lobbies if ctx.channel == lobby.channel):
            raise exceptions.NotCalledFromALobby
        return True

    return commands.check(predicate)


def is_not_called_from_lobby(lobbies):
    """Checks whether the channel this command is being called from is a lobby"""

    async def predicate(ctx):
        if any(lobby for lobby in lobbies if ctx.channel == lobby.channel):
            raise exceptions.CalledFromALobby
        return True

    return commands.check(predicate)


def user_not_in_lobby(lobbies):
    """Checks whether the caller is already in a lobby"""

    async def predicate(ctx):
        member = ctx.message.author

        for lobby in lobbies:
            if any(player for player in lobby.players if player.member == member):
                raise exceptions.DuplicatePlayer
            else:
                return True

    return commands.check(predicate)


def lobby_exists(lobbies):
    """Checks whether the requested lobby exists"""

    async def predicate(ctx):
        lobby_id = Lobby.get_id_from_string(ctx.message.content)
        try:
            Lobby.get_lobby_by_id(lobby_id, lobbies)
        except exceptions.LobbyNotFound:
            raise exceptions.LobbyNotFound
        return True

    return commands.check(predicate)
