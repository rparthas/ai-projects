from app.tools.weather_tool import get_weather_forecast

def get_weather(state: dict) -> dict:
    """Fetches the real weather forecast using the weather tool and updates the state."""
    print("---NODE: Fetching Real Weather---")
    
    # The tool defaults to Bengaluru, which is what we want for now.
    # In the future, this could take location from the state.
    weather_info = get_weather_forecast.invoke({})
    print(f"Weather info: {weather_info}")
    
    return {"weather_info": weather_info}
