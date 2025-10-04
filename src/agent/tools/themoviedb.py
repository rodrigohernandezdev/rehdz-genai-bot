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


@tool
def search_movie(query: str) -> str:
    """
    Searches for movies by title using The Movie Database (TMDb) API.

    Args:
        query: The movie title to search for

    Returns a formatted string with movie search results including title, release date, and overview.
    """
    url = f"{MOVIES_API_URL}/3/search/movie"
    auth_header = f"Bearer {MOVIEDB_KEY}"
    params = {
        "query": query,
        "language": "es",
        "page": 1
    }

    try:
        response = requests.get(
            url,
            headers={"Authorization": auth_header, "Content-Type": "application/json"},
            params=params
        )
        response.raise_for_status()

        data = response.json()
        results = data.get("results", [])

        if not results:
            return f"There is not result for: '{query}'."

        movie_list = []
        for movie in results[:5]:
            title = movie.get("title", "N/A")
            release_date = movie.get("release_date", "N/A")
            overview = movie.get("overview", "Sin descripción disponible")
            rating = movie.get("vote_average", "N/A")

            movie_info = f"*{title}* ({release_date})\n"
            movie_info += f"⭐ Calificación: {rating}/10\n"
            movie_info += f" Sinapsis {overview}\n"
            movie_list.append(movie_info)

        return "Search result:\n\n" + "\n---\n\n".join(movie_list)

    except requests.exceptions.RequestException as e:
        print(f"Error during movie search: {e}")
        return f"An error occurred while searching for movies"


themoviedb_tools = [get_movie_genres, search_movie]
