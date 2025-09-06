# Story: Implement Intelligent Activity Agent

## Description

This story focuses on making the Activity Agent intelligent. It will use a Language Model and the web search tool to dynamically find a real-world activity that matches the user's preferences.

## Tasks

- [ ] Modify the `find_activity` function in `app/agents/activity.py`.
- [ ] Import the `web_search` tool from `app.tools.search_tool` and the `llm` from `app.core.llm`.
- [ ] Design a prompt template that instructs the LLM to generate a search query and then select a single, suitable activity from the search results. The prompt should request the output in a specific JSON format (e.g., `{"name": "...", "address": "..."}`).
- [ ] Create and invoke a LangChain chain or agent that uses the LLM and the search tool.
- [ ] Implement robust parsing for the LLM's output to handle potential errors and ensure the activity data is correctly extracted.
- [ ] Update the state dictionary with the dynamically found activity. If no activity is found, the value should be `None`.
