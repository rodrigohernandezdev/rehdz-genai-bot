import requests
from langchain_core.tools import tool

from src.config import WEATHER_KEY

WEATHER_API_URL = "https://api.weatherapi.com/v1"


@tool
def get_weather_by_city(city) -> str:
    """
    Fetches the current weather for a given city using the WeatherAPI.
    Args:
        city (str): The name of the city to get the weather for.
    Returns:
        str: A formatted string with the current weather information.
    """
    endpoint = f"{WEATHER_API_URL}/current.json"
    params = {
        "key": {WEATHER_KEY},
        "q": city
    }
    try:
        response = requests.get(endpoint, params=params)
        if response.status_code == 200:
            data = response.json()

            location = data.get("location", {})
            current = data.get("current", {})
            if location and current:
                city_name = location.get("name", "Unknown location")
                country = location.get("country", "Unknown country")
                temp_c = current.get("temp_c", "N/A")
                condition = current.get("condition", {}).get("text", "N/A")
                humidity = current.get("humidity", "N/A")
                wind_kph = current.get("wind_kph", "N/A")
                feels_like = current.get("feelslike_c", "N/A")

                weather_info = (
                    f"El clima en {city_name}, {country}:\n"
                    f"- Temperatura: {temp_c}°C\n"
                    f"- Condición: {condition}\n"
                    f"- Humedad: {humidity}%\n"
                    f"- Viento: {wind_kph} kph\n"
                    f"- Sensación térmica: {feels_like}°C"
                )
                return weather_info
            else:
                return "No hay información disponible para esta ciudad."

        return "No se puede encontrar la ciudad especificada."
    except Exception as e:
        print(f"Error getting weather data: {e}")
        return "No se pudo obtener la información del clima."


weather_tools = [get_weather_by_city]
