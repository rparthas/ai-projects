# Story: Agent Implementation

## Description

Create the individual agents responsible for specific tasks in the planning process. These agents will be nodes in the final graph.

## Tasks

- [ ] **Weather Agent:**
    - [ ] Create the agent in `app/agents/weather.py`.
    - [ ] It should use the Weather Tool to get the forecast.
    - [ ] It should process the tool's output into a simple, human-readable string.

- [ ] **Activity Agent:**
    - [ ] Create the agent in `app/agents/activity.py`.
    - [ ] It should use the Search Tool to find age-appropriate activities.
    - [ ] It should process the search results to select one activity and extract its details (name, location).

- [ ] **Restaurant Agent:**
    - [ ] Create the agent in `app/agents/restaurant.py`.
    - [ ] It should use the Search Tool to find kid-friendly restaurants near the selected activity's location, filtering by dietary preference.
    - [ ] It should process the search results to select one restaurant and extract its details.
