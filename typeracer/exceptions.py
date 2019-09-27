from discord.ext import commands


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
