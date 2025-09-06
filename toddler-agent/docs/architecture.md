# Architecture Design: Toddler Activity Planner

## 1. Overview

This document outlines the software architecture for the Toddler Activity Planner, a multi-agent system designed to generate weekend plans for toddlers. The architecture is based on the requirements specified in the [Product Requirements Document](./prd.md).

The system follows a client-server model. A simple web frontend provides the user interface, and a Python backend hosts the multi-agent system built with LangChain.

## 2. High-Level Architecture

The architecture consists of three main layers:

1.  **Presentation Layer (Frontend):** A web-based user interface for user interaction.
2.  **Application Layer (Backend):** A Python web server that exposes an API and orchestrates the agentic workflow.
3.  **Tool/Service Layer:** A collection of external APIs and internal tools that the agents use to gather information.

```mermaid
graph TD
    subgraph User
        A[Web Browser]
    end

    subgraph Application Layer (Backend)
        B[API Server - FastAPI]
        C[Multi-Agent System - LangChain]
    end

    subgraph Tool/Service Layer
        D[Weather API - Open-Meteo]
        E[Web Search - DuckDuckGo]
        F[Geospatial Tools - Nominatim]
    end

    A -- HTTP Request --> B
    B -- Invokes --> C
    C -- Uses Tools --> D
    C -- Uses Tools --> E
    C -- Uses Tools --> F
    B -- HTTP Response --> A
```

## 3. Component Breakdown

### 3.1. Frontend

*   **Description:** A single-page application (SPA) that allows users to input their preferences and displays the generated activity plan.
*   **Technology:** To keep it simple, we will use **HTML, CSS, and vanilla JavaScript** to create the form and display the results. A simple `fetch` call will be used to communicate with the backend API.
*   **Responsibilities:**
    *   Render an input form for toddler's age, dietary preferences, and location/area in Bengaluru.
    *   Send user preferences to the backend API.
    *   Display the formatted plan received from the backend.
    *   Show loading states and handle errors gracefully.

### 3.2. Backend

*   **Description:** A Python-based server that provides the core logic of the application.
*   **Technology:** **FastAPI** is recommended for its performance, ease of use, and automatic OpenAPI documentation, which is useful for development.
*   **Responsibilities:**
    *   Expose a RESTful API endpoint (e.g., `/plan-weekend`) to receive requests from the frontend.
    *   Validate user input.
    *   Initialize and run the multi-agent system with the user's preferences.
    *   Return the final plan as a JSON response.

### 3.3. Multi-Agent System

*   **Description:** The core of the backend, built using the **LangChain** framework (specifically, `langgraph` for robust state management). It implements a hierarchical and collaborative agent workflow.
*   **Architecture:** A stateful graph where each node represents an agent or a processing step. The state will be passed between nodes, allowing for a collaborative workflow.

    *   **State Object:** A central Python data class will hold the state of the planning process.
        ```python
        class PlanState:
            toddler_age: int
            dietary_preference: str
            location: str
            weather_info: str = None
            activity: dict = None
            restaurant: dict = None
            final_plan: str = None
            error_message: str = None
        ```

    *   **Graph Flow:**
        1.  **Orchestrator:** The entry point of the graph. It receives the initial user request and populates the initial state.
        2.  **Weather Agent Node:** Runs the Weather Agent to fetch the forecast. Updates `state.weather_info`.
        3.  **Activity Agent Node:** Runs the Activity Agent to find a suitable activity. Updates `state.activity`.
        4.  **Conditional Edge (Activity Found?):**
            *   If `state.activity` is found, proceed to the Restaurant Agent.
            *   If not, proceed directly to the Response Mixer to generate an error message.
        5.  **Restaurant Agent Node:** Runs the Restaurant Agent, using `state.activity['location']` as input. Updates `state.restaurant`.
        6.  **Response Mixer Node:** The final node. It synthesizes all information from the state (`weather_info`, `activity`, `restaurant`) into a cohesive, user-friendly plan. Updates `state.final_plan`.

## 4. Agent Design

Each agent will be a LangChain component, equipped with specific tools and a clear objective.

*   **Orchestrator Agent:**
    *   **Role:** Manages the overall workflow. In `langgraph`, this is the graph definition itself.
    *   **Input:** User query (e.g., "plan a fun Saturday"), toddler's age, dietary preference.
    *   **Output:** The initial state for the agentic graph.

*   **Weather Agent:**
    *   **LLM:** A lightweight model (e.g., Llama 3 8B) is sufficient.
    *   **Tool:** A Python function that calls the **Open-Meteo API** for Bengaluru.
    *   **Input:** Location (Bengaluru) and date.
    *   **Output:** A string summarizing the weather (e.g., "Sunny with a high of 28°C").

*   **Activity Agent:**
    *   **LLM:** A capable model for reasoning and web search (e.g., Llama 3 70B or Mixtral).
    *   **Tool:** A **DuckDuckGo search tool** to find "toddler-friendly activities in [location]".
    *   **Input:** Toddler's age, location.
    *   **Output:** A dictionary with activity details: `{ "name": "Cubbon Park", "type": "Park", "location": "Kasturba Road, Bengaluru" }`.

*   **Restaurant Agent:**
    *   **LLM:** Similar to the Activity Agent.
    *   **Tool:** A **DuckDuckGo search tool** to find "[dietary preference] kid-friendly restaurants near [activity location]".
    *   **Input:** Activity location, dietary preference.
    *   **Output:** A dictionary with restaurant details: `{ "name": "Corner House", "cuisine": "Desserts", "location": "Residency Road, Bengaluru" }`.

*   **Response Mixer Agent:**
    *   **LLM:** A capable model for creative generation.
    *   **Role:** This agent does not use tools. It synthesizes the information gathered by other agents.
    *   **Input:** The final state object containing weather, activity, and restaurant information.
    *   **Output:** A formatted Markdown string representing the final plan with a schedule.

## 5. Proposed Project Structure

```
toddler-agent/
├── docs/
│   ├── prd.md
│   └── architecture.md
├── app/
│   ├── __init__.py
│   ├── main.py             # FastAPI application
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── weather.py
│   │   ├── activity.py
│   │   ├── restaurant.py
│   │   └── graph.py          # LangGraph orchestration
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── weather_tool.py
│   │   └── search_tool.py
│   └── core/
│       ├── __init__.py
│       └── config.py         # Configuration management (API keys, etc.)
├── static/                 # For simple frontend
│   ├── index.html
│   └── styles.css
└── requirements.txt
```