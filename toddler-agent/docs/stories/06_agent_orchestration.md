# Story: Agent Orchestration

## Description

Build the `langgraph` graph to orchestrate the agents, manage the application state, and produce the final plan.

## Tasks

- [ ] **State Definition:**
    - [ ] Define the `PlanState` TypedDict or Pydantic class in `app/agents/graph.py`.

- [ ] **Graph Construction:**
    - [ ] In `app/agents/graph.py`, create a new `StatefulGraph`.
    - [ ] Add the Weather, Activity, and Restaurant agents as nodes.
    - [ ] Implement the Response Mixer logic in a final node to synthesize the results into a formatted plan.
    - [ ] Define the edges connecting the nodes in the correct sequence.
    - [ ] Add a conditional edge to handle the case where no activity is found.

- [ ] **API Integration:**
    - [ ] In `app/main.py`, import and compile the graph.
    - [ ] Call the graph from within the `/plan-weekend` endpoint, passing the user's preferences.
    - [ ] Return the final plan from the graph's output.
