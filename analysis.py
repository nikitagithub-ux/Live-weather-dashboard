import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np
import os

def plot_temperature_trend(df, city):
    """Plot temperature trend with actual regression line for the given city."""
    if df.empty:
        return

    city_df = df[df["city"] == city].copy()
    if city_df.empty:
        return

    city_df["date"] = pd.to_datetime(city_df["date"])
    city_df = city_df.sort_values("date").drop_duplicates("date")

    # Convert timestamps to Unix seconds for regression
    city_df["timestamp"] = city_df["date"].astype(np.int64) // 10**9

    X = city_df[["timestamp"]].values
    y = city_df["temperature"].values

    plt.figure(figsize=(9, 4))
    plt.plot(city_df["date"], y, marker="o", color="#f77f00", linewidth=2, label="Actual Temp")

    # Only draw regression line if we have enough points
    if len(city_df) >= 2:
        model = LinearRegression()
        model.fit(X, y)
        trend_y = model.predict(X)
        plt.plot(city_df["date"], trend_y, linestyle="--", color="#0077b6", linewidth=1.5, label="Trend (Regression)")

    plt.title(f"Temperature Trend — {city}", fontsize=13)
    plt.xlabel("Date / Time")
    plt.ylabel("Temperature (°C)")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()

    os.makedirs("static", exist_ok=True)
    plt.savefig("static/temp_trend.png")
    plt.close()


def predict_next_hour(df, city):
    city_df = df[df["city"] == city].copy()
    if len(city_df) < 2:
        return "Not enough data yet"

    city_df["date"] = pd.to_datetime(city_df["date"])
    city_df = city_df.sort_values("date").drop_duplicates("date")
    city_df = city_df.tail(10) 

    # Check if any gap between readings is larger than 30 minutes
    time_diffs = city_df["date"].diff().dropna()
    max_gap_minutes = time_diffs.max().total_seconds() / 60
    if max_gap_minutes > 30:
        return "Not enough continuous data to predict"

    city_df["timestamp"] = city_df["date"].astype(np.int64) // 10**9
    city_df["minutes"] = (city_df["timestamp"] - city_df["timestamp"].iloc[0]) / 60

    X = city_df[["minutes"]].values
    y = city_df["temperature"].values

    model = LinearRegression()
    model.fit(X, y)

    next_minutes = city_df["minutes"].iloc[-1] + 60
    predicted = model.predict([[next_minutes]])[0]

    return f"{round(predicted, 2)} °C"


def generate_insight(city_data):
    """Compare the last two temperature readings and describe the change."""
    if city_data.empty or len(city_data) < 2:
        return "Not enough data for insights yet."

    city_data = city_data.copy()
    city_data["date"] = pd.to_datetime(city_data["date"])
    city_data = city_data.sort_values("date")

    prev_temp = city_data["temperature"].iloc[-2]
    latest_temp = city_data["temperature"].iloc[-1]
    change = latest_temp - prev_temp

    if abs(change) < 0.5:
        return "Temperature is stable — no significant change since last reading."
    elif change > 0:
        return f"🌡️ Temperature has risen by {round(change, 2)}°C since the last reading."
    else:
        return f"❄️ Temperature has dropped by {round(abs(change), 2)}°C since the last reading."