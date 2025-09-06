# Story: Agent Implementation

## Description

Create the individual agents responsible for specific tasks in the planning process. These agents will be nodes in the final graph.

## Tasks

- [x] **Weather Agent:**
    - [x] Create the agent in `app/agents/weather.py`.
    - [x] It should use the Weather Tool to get the forecast.
    - [x] It should process the tool's output into a simple, human-readable string.

- [x] **Activity Agent:**
    - [x] Create the agent in `app/agents/activity.py`.
    - [x] It should use the Search Tool to find age-appropriate activities.
    - [x] It should process the search results to select one activity and extract its details (name, location).

- [x] **Restaurant Agent:**
    - [x] Create the agent in `app/agents/restaurant.py`.
    - [x] It should use the Search Tool to find kid-friendly restaurants near the selected activity's location, filtering by dietary preference.
    - [x] It should process the search results to select one restaurant and extract its details.