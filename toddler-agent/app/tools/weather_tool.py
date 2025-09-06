import requests
from langchain.tools import tool

@tool
def get_weather_forecast(latitude: float = 12.97, longitude: float = 77.59) -> str:
    """Fetches the 3-day weather forecast for a given latitude and longitude (defaults to Bengaluru).
    Returns a string summarizing the weather conditions.
    """
    try:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "daily": "weathercode,temperature_2m_max,temperature_2m_min",
            "timezone": "Asia/Kolkata",
            "forecast_days": 3
        }
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()

        # Process and format the data into a human-readable summary
        summary = "Weather Forecast for the next 3 days:\n"
        for i in range(len(data['daily']['time'])):
            date = data['daily']['time'][i]
            max_temp = data['daily']['temperature_2m_max'][i]
            min_temp = data['daily']['temperature_2m_min'][i]
            summary += f"- {date}: Max Temp: {max_temp}°C, Min Temp: {min_temp}°C\n"
        
        return summary

    except requests.exceptions.RequestException as e:
        return f"Error fetching weather data: {e}"
    except (KeyError, IndexError) as e:
        return f"Error processing weather data: {e}"

