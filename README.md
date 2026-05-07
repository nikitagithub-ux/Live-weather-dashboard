# Live Weather Dashboard

A Python web app that fetches real-time weather data and predicts the next hour's temperature using linear regression.

## Features
- Live weather data via OpenWeather API
- City autocomplete with debounced search
- 1-hour temperature forecasting using linear regression
- Data continuity validation before predicting
- Temperature trend chart with regression line
- Insight generation comparing consecutive readings

## Tech Stack
Python, Flask, scikit-learn, Pandas, Matplotlib, OpenWeather API

## Setup
1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file with your API key: MY_API_KEY=your_openweather_api_key
4. Run: `python app.py`
5. Open `http://localhost:5000`
