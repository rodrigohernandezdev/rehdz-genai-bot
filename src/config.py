import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_API")
GEMINI_KEY = os.getenv("GEMINI_KEY")
MOVIEDB_KEY = os.getenv("MOVIEDB_KEY")
WEATHER_KEY = os.getenv("WEATHER_KEY")

# Conversation states
MAIN_MENU, MOVIES_MENU, MUSIC_MENU = range(3)
