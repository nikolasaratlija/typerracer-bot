from discord import Member


# can't figure out a way to simply extend discord.Member
class Player:
    def __init__(self, member: Member):
        self.member: Member = member
        self.finished = False
