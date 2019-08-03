# should prevents users from being able to copy-paste the text and cheat the game
encryption_character = "_"


def encrypt(string: str):
    return string.replace(" ", encryption_character)


def decrypt(encrypted_string: str):
    return encrypted_string.replace(encryption_character, " ")
