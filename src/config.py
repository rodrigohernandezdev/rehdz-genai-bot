import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_API")

# Conversation states
MAIN_MENU, MOVIES_MENU, MUSIC_MENU = range(3)
