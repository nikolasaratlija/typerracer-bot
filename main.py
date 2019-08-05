from os import getenv
from dotenv import load_dotenv

from Typeracer import typeracer

load_dotenv()
TOKEN = getenv("DISCORD_BOT_TOKEN")

typeracer.run(TOKEN)
