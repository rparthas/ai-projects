# Story: Agent Tools

## Description

Implement the tools that the agents will use to gather external information.

## Tasks

- [ ] **Weather Tool:**
    - [ ] Create a function in `app/tools/weather_tool.py`.
    - [ ] The function should call the Open-Meteo API using the `requests` library to get the weather forecast for Bengaluru.
    - [ ] Wrap this function in a LangChain `Tool`.

- [ ] **Search Tool:**
    - [ ] Create a function in `app/tools/search_tool.py`.
    - [ ] The function should use the `duckduckgo-search` library to perform a web search.
    - [ ] Wrap this function in a LangChain `Tool` that can be used by the Activity and Restaurant agents.
