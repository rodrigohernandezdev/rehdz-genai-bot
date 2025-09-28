import requests
from langchain_core.tools import tool

from src.config import MOVIEDB_KEY

MOVIES_API_URL = "https://api.themoviedb.org"


@tool
def get_movie_genres() -> str:
    """
    Fetches the list of movie genres from The Movie Database (TMDb) API.
    Returns a formatted string with the list of genres.
    """
    url = f"{MOVIES_API_URL}/3/genre/movie/list?language=es"
    auth_header = f"Bearer {MOVIEDB_KEY}"
    try:
        response = requests.get(url, headers={"Authorization": auth_header, "Content-Type": "application/json"})
        response.raise_for_status()

        data = response.json()
        genres = data.get("genres", [])

        if not genres:
            return "No movie genres found."

        genre_list = [f"- {genre['name']} (ID: {genre['id']})" for genre in genres]
        return "Here is the list of available movie genres:\n\n" + "\n".join(genre_list)

    except requests.exceptions.RequestException as e:
        return f"An error occurred while fetching movie genres: {e}"


themoviedb_tools = [get_movie_genres]
