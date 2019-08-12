from discord.ext import commands


# region exceptions


class NoParticipants(Exception):
    pass


class DuplicatePlayer(commands.CheckFailure):
    pass


class NotCalledFromALobby(commands.CheckFailure):
    pass


class CalledFromALobby(commands.CheckFailure):
    pass


class NotAHost(commands.CheckFailure):
    pass


class LobbyNotFound(commands.CheckFailure):
    pass


# endregion exceptions

def is_lobby_host(lobbies):
    """Checks whether the caller of this command is a host of a lobby"""

    async def predicate(ctx):
        user = ctx.message.author

        if not any(lobby for lobby in lobbies if user == lobby.host):
            raise NotAHost
        return True

    return commands.check(predicate)


def is_called_from_lobby(lobbies):
    """Checks whether the channel this command is being called from is a lobby"""

    async def predicate(ctx):
        if not any(lobby for lobby in lobbies if ctx.channel == lobby.channel):
            raise NotCalledFromALobby
        return True

    return commands.check(predicate)


def is_not_called_from_lobby(lobbies):
    """Checks whether the channel this command is being called from is a lobby"""

    async def predicate(ctx):
        if any(lobby for lobby in lobbies if ctx.channel == lobby.channel):
            raise CalledFromALobby
        return True

    return commands.check(predicate)


def user_not_in_lobby(lobbies):
    """Checks whether the caller is already in a lobby"""

    async def predicate(ctx):
        player = ctx.message.author

        if any(lobby for lobby in lobbies if player in lobby.players):
            raise DuplicatePlayer
        return True

    return commands.check(predicate)


def lobby_exists(lobbies):
    """Checks whether the requested lobby exists"""

    async def predicate(ctx):
        # TODO: only works with lobby ids that are 2 characters long
        if not any(lobby for lobby in lobbies if ctx.message.content[-2:] == lobby.lobby_id):
            raise LobbyNotFound
        return True

    return commands.check(predicate)
