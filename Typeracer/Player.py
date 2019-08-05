from discord import Member


class Player:
    def __init__(self, member: Member):
        self.member_id = member.id
        self.finished = False
