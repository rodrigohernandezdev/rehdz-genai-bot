# rehdz-genai-bot

An AI-powered Telegram bot that provides entertainment services including movie information, weather updates, date information, and general conversation capabilities.

## Features

- 🎬 Movie search: Find detailed information about movies including ratings, summaries, and more
- 🌤️ Weather updates: Get current weather information for any city
- 📅 Date information: Get current date with additional information and motivational quotes
- 🤖 AI-powered conversations: Engage in natural conversations with the bot
- 📋 Interactive menu: Navigate through different features using inline keyboards

## Setup Instructions

### Prerequisites

1. Copy the `.env.example` file to create your own `.env` file:
   ```bash
   cp .env.example .env
   ```

2. Fill in the required API keys in the `.env` file:
   - `TELEGRAM_API`: Your Telegram bot token
   - `GEMINI_KEY`: Google Gemini API key
   - `MOVIEDB_KEY`: TheMovieDB API key
   - `WEATHER_KEY`: Weather API key

3. The project includes a `uv.lock` file for dependency management, ensuring consistent builds across environments.

### Running Locally

#### Using UV (Recommended)

1. Install dependencies:
   ```bash
   uv sync
   ```

2. Run the bot:
   ```bash
   uv run python main.py
   ```

#### Using Python and pip

1. Create a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install python-telegram-bot dotenv langchain langchain-community langchain-google-genai requests
   ```

3. Run the bot:
   ```bash
   python main.py
   ```

### Running with Docker

1. Build the Docker image:
   ```bash
   docker build -t rehdz-genai-bot .
   ```

2. Run the container with environment variables:
   ```bash
   docker run -d --name rehdz-genai-bot-container \
     -e TELEGRAM_API="your_telegram_api_key" \
     -e GEMINI_KEY="your_gemini_key" \
     -e MOVIEDB_KEY="your_moviedb_key" \
     -e WEATHER_KEY="your_weather_key" \
     rehdz-genai-bot
   ```

Alternatively, you can run the container by mounting an environment file:
   ```bash
   docker run -d --name rehdz-genai-bot-container \
     --env-file .env \
     rehdz-genai-bot
   ```

## Tools Used

1. Python3
2. UV (as package and project manager)
3. LangChain
4. TheMovieDB
5. Python Telegram BOT