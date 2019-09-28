from discord.ext import commands


class NoParticipants(commands.CheckFailure):
    pass


class DuplicatePlayer(commands.CheckFailure):
    pass


class NotCalledFromLobby(commands.CheckFailure):
    pass


class CalledFromALobby(commands.CheckFailure):
    pass


class NotHostOfLobby(commands.CheckFailure):
    pass


class AlreadyHost(commands.CheckFailure):
    pass


class LobbyNotFound(commands.CheckFailure):
    pass
