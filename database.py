import pandas as pd
import os

FILE_PATH = "data/weather.csv"

def save_data(new_data):
    """Save a weather data dict to CSV. Includes city, wind_speed, description."""
    os.makedirs("data", exist_ok=True)
    df = pd.DataFrame([new_data])
    if os.path.exists(FILE_PATH):
        df.to_csv(FILE_PATH, mode='a', header=False, index=False)
    else:
        df.to_csv(FILE_PATH, index=False)

def load_data():
    """Load all historical weather data from CSV."""
    if os.path.exists(FILE_PATH):
        return pd.read_csv(FILE_PATH)
    return pd.DataFrame(columns=["date", "city", "temperature", "humidity", "wind_speed", "description"])