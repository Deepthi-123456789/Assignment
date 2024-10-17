import time
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Constants
API_KEY = '5fcd5d8ec5391ea06fbcaf4029a42b73'  # Replace with your OpenWeatherMap API key
CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']
INTERVAL = 300  # 5 minutes in seconds
ALERT_THRESHOLD_TEMP = 35.0  # User-configurable threshold for temperature
HUMIDITY_THRESHOLD = 80  # Example: alert if humidity exceeds 80%

# Initialize lists to hold weather and forecast data
weather_data = []
forecast_data = []

# Function to fetch current weather data from OpenWeatherMap API
def fetch_weather_data(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data for {city}: {response.status_code}")
        return None

# Function to fetch weather forecast data from OpenWeatherMap API
def fetch_forecast_data(city):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching forecast data for {city}: {response.status_code}")
        return None

# Function to process weather data
def process_weather_data(data):
    if data and 'main' in data and 'weather' in data:
        main = data['main']
        weather = data['weather'][0]['main']
        dt = datetime.fromtimestamp(data['dt']).date()

        # Convert temperatures from Kelvin to Celsius and round off values
        temp_c = round(main['temp'] - 273.15, 2)
        feels_like_c = round(main['feels_like'] - 273.15, 2)
        humidity = main.get('humidity', None)
        wind_speed = data.get('wind', {}).get('speed', None)

        weather_data.append({
            'date': dt,
            'city': data['name'],
            'temp': temp_c,
            'feels_like': feels_like_c,
            'humidity': humidity,
            'wind_speed': wind_speed,
            'condition': weather
        })

        # Enhanced structured output
        print(f"City: {data['name']}")
        print(f"  Date: {dt}")
        print(f"  Temperature: {temp_c}°C (Feels like: {feels_like_c}°C)")
        print(f"  Humidity: {humidity}%")
        print(f"  Wind Speed: {wind_speed} m/s")
        print(f"  Condition: {weather}\n")
    else:
        print(f"Invalid data received: {data}")

# Function to process forecast data
def process_forecast_data(data):
    if data and 'list' in data:
        for forecast in data['list']:
            dt = datetime.fromtimestamp(forecast['dt'])
            main = forecast['main']
            weather = forecast['weather'][0]['main']

            temp_c = round(main['temp'] - 273.15, 2)
            feels_like_c = round(main['feels_like'] - 273.15, 2)
            humidity = main.get('humidity', None)
            wind_speed = forecast.get('wind', {}).get('speed', None)

            forecast_data.append({
                'datetime': dt,
                'city': data['city']['name'],
                'temp': temp_c,
                'feels_like': feels_like_c,
                'humidity': humidity,
                'wind_speed': wind_speed,
                'condition': weather
            })
    else:
        print(f"Invalid forecast data received: {data}")

# Function to calculate daily weather summary
def calculate_daily_summary():
    df = pd.DataFrame(weather_data)
    if not df.empty:
        daily_summary = df.groupby(['date', 'city']).agg(
            avg_temp=('temp', 'mean'),
            max_temp=('temp', 'max'),
            min_temp=('temp', 'min'),
            avg_humidity=('humidity', 'mean'),
            max_wind_speed=('wind_speed', 'max'),
            dominant_condition=('condition', lambda x: x.value_counts().idxmax())
        ).reset_index()
        return daily_summary
    return pd.DataFrame()  # Return an empty dataframe if no data

# Function to check alert conditions
def check_alerts(city, temp, humidity):
    if temp > ALERT_THRESHOLD_TEMP:
        print(f"Alert! Temperature in {city} exceeds {ALERT_THRESHOLD_TEMP}°C: {temp}°C.")
    if humidity and humidity > HUMIDITY_THRESHOLD:
        print(f"Alert! Humidity in {city} exceeds {HUMIDITY_THRESHOLD}%: {humidity}%.")

# Function to visualize daily weather summaries
def plot_weather_summary(daily_summary):
    if not daily_summary.empty:
        plt.figure(figsize=(12, 6))
        for city in daily_summary['city'].unique():
            city_data = daily_summary[daily_summary['city'] == city]
            plt.plot(city_data['date'], city_data['max_temp'], label=f'Max Temp in {city}', linestyle='--', marker='o')
            plt.plot(city_data['date'], city_data['min_temp'], label=f'Min Temp in {city}', linestyle='--', marker='x')

        plt.title('Daily Max and Min Temperatures')
        plt.xlabel('Date')
        plt.ylabel('Temperature (°C)')
        plt.legend()
        plt.grid()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

# Function to visualize forecast data
def plot_forecast_data():
    df = pd.DataFrame(forecast_data)
    if not df.empty:
        plt.figure(figsize=(12, 6))
        for city in df['city'].unique():
            city_forecast = df[df['city'] == city]
            plt.plot(city_forecast['datetime'], city_forecast['temp'], label=f'Temp Forecast in {city}')
            plt.fill_between(city_forecast['datetime'], city_forecast['temp'], city_forecast['feels_like'], alpha=0.3)

        plt.title('Forecasted Temperatures')
        plt.xlabel('Datetime')
        plt.ylabel('Temperature (°C)')
        plt.legend()
        plt.grid()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

# Main loop to continuously fetch and process data
while True:
    # Fetch and process current weather data
    for city in CITIES:
        data = fetch_weather_data(city)
        process_weather_data(data)
        if data and 'main' in data:
            current_temp = data['main']['temp'] - 273.15
            humidity = data['main'].get('humidity', None)
            check_alerts(city, current_temp, humidity)

        # Fetch and process forecast data
        forecast = fetch_forecast_data(city)
        process_forecast_data(forecast)

    # Generate and plot daily summary
    daily_summary = calculate_daily_summary()
    if not daily_summary.empty:
        print(daily_summary)  # Optional: Print daily summary for inspection
        plot_weather_summary(daily_summary)

    # Plot forecast data
    if forecast_data:
        plot_forecast_data()

    # Wait for the next interval
    # time.sleep(INTERVAL)
