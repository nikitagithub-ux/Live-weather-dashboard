from flask import Flask, render_template, request, jsonify
from fetch_weather import fetch_weather, API_KEY
from database import save_data, load_data
from analysis import plot_temperature_trend, predict_next_hour, generate_insight
import requests

app = Flask(__name__)

@app.route("/autocomplete")
def autocomplete():
    query = request.args.get("q", "").strip()
    if len(query) < 2:
        return jsonify([])

    url = "http://api.openweathermap.org/geo/1.0/direct"
    params = {"q": query, "limit": 8, "appid": API_KEY}
    resp = requests.get(url, params=params)
    data = resp.json()

    suggestions = []
    for item in data:
        # Build a nice label: "London, England, GB"
        parts = [item.get("name", "")]
        if item.get("state"):
            parts.append(item["state"])
        parts.append(item.get("country", ""))
        label = ", ".join(p for p in parts if p)
        suggestions.append({"label": label, "value": item["name"]})

    return jsonify(suggestions)


@app.route("/", methods=["GET"])
def home():
    city = request.args.get("city", "London")

    weather = fetch_weather(city)
    if "error" in weather:
        return render_template("index.html", error=weather["error"], city=city)

    save_data(weather)
    df = load_data()
    plot_temperature_trend(df, city)
    pred = predict_next_hour(df, city)
    city_data = df[df["city"] == city]
    insights = generate_insight(city_data)

    return render_template(
        "index.html",
        temperature=weather["temperature"],
        humidity=weather["humidity"],
        wind_speed=weather.get("wind_speed", "N/A"),
        description=weather.get("description", ""),
        prediction=pred,
        city=city,
        insights=insights,
    )

if __name__ == "__main__":
    app.run(debug=True)

