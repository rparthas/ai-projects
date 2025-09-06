# Story: Implement Intelligent Weather Agent

## Description

This story involves replacing the placeholder logic in the Weather Agent with a real implementation that calls the `get_weather_forecast` tool. This will provide real-time weather data to the plan.

## Tasks

- [ ] Modify the `get_weather` function in `app/agents/weather.py`.
- [ ] Import the `get_weather_forecast` tool from `app.tools.weather_tool`.
- [ ] Invoke the tool within the function.
- [ ] Place the real weather forecast string returned by the tool into the `weather_info` key of the state dictionary.
