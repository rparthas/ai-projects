# Story: Agent Orchestration

## Description

Build the `langgraph` graph to orchestrate the agents, manage the application state, and produce the final plan.

## Tasks

- [x] **State Definition:**
    - [x] Define the `PlanState` TypedDict or Pydantic class in `app/agents/graph.py`.

- [x] **Graph Construction:**
    - [x] In `app/agents/graph.py`, create a new `StatefulGraph`.
    - [x] Add the Weather, Activity, and Restaurant agents as nodes.
    - [x] Implement the Response Mixer logic in a final node to synthesize the results into a formatted plan.
    - [x] Define the edges connecting the nodes in the correct sequence.
    - [x] Add a conditional edge to handle the case where no activity is found.

- [x] **API Integration:**
    - [x] In `app/main.py`, import and compile the graph.
    - [x] Call the graph from within the `/plan-weekend` endpoint, passing the user's preferences.
    - [x] Return the final plan from the graph's output.