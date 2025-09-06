# Story: Agent Tools

## Description

Implement the tools that the agents will use to gather external information.

## Tasks

- [x] **Weather Tool:**
    - [x] Create a function in `app/tools/weather_tool.py`.
    - [x] The function should call the Open-Meteo API using the `requests` library to get the weather forecast for Bengaluru.
    - [x] Wrap this function in a LangChain `Tool`.

- [x] **Search Tool:**
    - [x] Create a function in `app/tools/search_tool.py`.
    - [x] The function should use the `duckduckgo-search` library to perform a web search.
    - [x] Wrap this function in a LangChain `Tool` that can be used by the Activity and Restaurant agents.