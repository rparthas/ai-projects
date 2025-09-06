# This file will contain the logic for the Weather Agent node.

def get_weather(state: dict) -> dict:
    """Fetches the weather and updates the state."""
    print("---NODE: Fetching Weather---")
    # In the future, this will call the weather tool.
    weather_info = "It's going to be sunny!"
    return {"weather_info": weather_info}
