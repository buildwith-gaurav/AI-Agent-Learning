def multiply(a:int , b:int) -> int:
    """multiply two numbers"""
    return a*b


def add(a:int , b:int) -> int:
    """add two numbers"""
    return a+b

import requests
def get_weather(city:str) -> str:
    """get the current weather for city"""
    geo_url ="https://geocoding-api.open-meteo.com/v1/search"
    geo_params ={
        "name": city,
        "count": 1,
        "language":"en",
        "format":"json"
    }
    geo_response = requests.get(geo_url, params=geo_params)
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
        params=weather_params
    )
    weather_data = weather_response.json()

    current = weather_data["current"]

    temperature = current["temperature_2m"]
    wind_speed = current["wind_speed_10m"]

    return (
        f"Weather in {city}: "
        f"{temperature}°C, "
        f"wind speed {wind_speed} km/h."
    )




