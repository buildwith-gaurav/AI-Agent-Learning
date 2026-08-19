def multiply(a:int , b:int) -> int:
    """multiply two numbers"""
    return a*b


def add(a:int , b:int) -> int:
    """add two numbers"""
    return a+b

import requests


def get_weather(city: str) -> str:
    """Get the current weather for a city."""

    try:
        geo_url = "https://geocoding-api.open-meteo.com/v1/search"

        geo_params = {
            "name": city,
            "count": 1,
            "language": "en",
            "format": "json"
        }

        geo_response = requests.get(
            geo_url,
            params=geo_params,
            timeout=10
        )

        geo_response.raise_for_status()

        geo_data = geo_response.json()

        if "results" not in geo_data:
            return f"Could not find the city: {city}"

        location = geo_data["results"][0]

        latitude = location["latitude"]
        longitude = location["longitude"]

        weather_url = "https://api.open-meteo.com/v1/forecast"

        weather_params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,wind_speed_10m"
        }

        weather_response = requests.get(
            weather_url,
            params=weather_params,
            timeout=10
        )

        weather_response.raise_for_status()

        weather_data = weather_response.json()

        current = weather_data["current"]

        temperature = current["temperature_2m"]
        wind_speed = current["wind_speed_10m"]

        return {
    "city": city,
    "temperature": temperature,
    "wind_speed": wind_speed
}

    except requests.RequestException:
        return "Weather service is temporarily unavailable. Please try again later."

    except Exception:
        return "Something went wrong while getting the weather."


