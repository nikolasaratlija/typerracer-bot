from os import getenv
from dotenv import load_dotenv

from typeracer import typeracer

load_dotenv()
TOKEN = getenv("DISCORD_BOT_TOKEN")

typeracer.run(TOKEN)
