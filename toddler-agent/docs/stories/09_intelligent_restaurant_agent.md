# Story: Implement Intelligent Restaurant Agent

## Description

This story makes the Restaurant Agent intelligent. It will find a real, kid-friendly restaurant located near the activity chosen by the Activity Agent, based on the user's dietary preferences.

## Tasks

- [ ] Modify the `find_restaurant` function in `app/agents/restaurant.py`.
- [ ] Import the `web_search` tool and the `llm`.
- [ ] Access the chosen activity's location and the user's dietary preferences from the state.
- [ ] Design a prompt template that instructs the LLM to find a suitable restaurant based on this context. The prompt should request the output in a specific JSON format.
- [ ] Create and invoke a LangChain chain or agent for this task.
- [ ] Implement robust parsing for the LLM's output.
- [ ] Update the state dictionary with the dynamically found restaurant. If no suitable restaurant is found, the value should be `None`.
