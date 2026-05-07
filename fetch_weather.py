import requests
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("MY_API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def fetch_weather(city="London"):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if "main" not in data:
        return {"error": data.get("message", "Unknown error")}

    weather_data = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "city": city,
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data.get("wind", {}).get("speed", None),
        "description": data["weather"][0]["description"].capitalize() if "weather" in data else "N/A"
    }
    return weather_data

if __name__ == "__main__":
    weather = fetch_weather("London")
    print(weather)