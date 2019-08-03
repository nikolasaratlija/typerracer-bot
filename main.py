from os import getenv

from dotenv import load_dotenv

from Typeracer import Typeracer

load_dotenv()
TOKEN = getenv("DISCORD_BOT_TOKEN")

client = Typeracer()
client.run(TOKEN)
