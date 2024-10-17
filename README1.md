The Weather Monitoring System fetches real-time weather data and forecasts for multiple cities using the OpenWeatherMap API. It processes the data to generate daily summaries, checks for alert conditions based on user-defined thresholds, and visualizes the results using Matplotlib.

Table of Contents::
---------------------
Features
Requirements
Setup
Usage
Data Processing
Alert System
Visualization
Functions Overview
License


Features::
---------------
Fetch current weather data for multiple cities.
Retrieve and process 5-day weather forecast data.
Calculate daily summaries, including average, maximum, and minimum temperatures.
Check for alert conditions based on user-defined thresholds for temperature and humidity.
Visualize daily summaries and forecast data using Matplotlib.

Requirements::pip install requests pandas matplotlib
---------------------------------------------
Python 3.x
requests
pandas
matplotlib

Setup::
-------------
Obtain an API Key: Sign up for an OpenWeatherMap API key here.
Update the API Key: Replace the placeholder API_KEY in the code with your actual API key.

Usage::
---------
Run the script to start fetching and processing weather data:
python weather_monitor.py



Data Processing::
-----------------
The system fetches current weather data and forecasts using the OpenWeatherMap API. The following functions are responsible for this:

fetch_weather_data(city): Retrieves current weather data for the specified city.
fetch_forecast_data(city): Retrieves 5-day weather forecast data for the specified city.
process_weather_data(data): Processes the current weather data to extract relevant metrics and store them in a structured format.
process_forecast_data(data): Processes the forecast data and appends it to the forecast list.

Alert System ::
---------------------
The system checks for alert conditions after fetching current weather data. Alerts are triggered based on:

Temperature Alert: If the temperature exceeds a user-defined threshold (default is 35°C).
Humidity Alert: If the humidity exceeds a user-defined threshold (default is 80%).

Visualization::
---------------
The system visualizes daily weather summaries and forecast data using Matplotlib:

plot_weather_summary(daily_summary): Plots daily maximum and minimum temperatures for each city.
plot_forecast_data(): Plots forecasted temperatures over the next few days, including fills between the forecasted and feels-like temperatures.



Functions Overview::
------------------------
fetch_weather_data(city): Fetches current weather data for the specified city.
fetch_forecast_data(city): Fetches 5-day weather forecast data for the specified city.
process_weather_data(data): Processes the current weather data and stores it in a structured format.
process_forecast_data(data): Processes forecast data and appends it to the forecast list.
calculate_daily_summary(): Generates daily summaries from the collected weather data.
check_alerts(city, temp, humidity): Checks if the current temperature or humidity exceeds defined thresholds and triggers alerts.
plot_weather_summary(daily_summary): Visualizes daily weather summaries.
plot_forecast_data(): Visualizes forecast data.