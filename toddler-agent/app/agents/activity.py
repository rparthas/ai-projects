import json
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage

from app.tools.search_tool import web_search
from app.core.llm import llm

def find_activity(state: dict) -> dict:
    """
    Finds a suitable activity using a tool-calling agent.
    """
    print("---NODE: Finding Real Activity---")
    child_age = state.get("child_age")
    activity_types = state.get("activity_types")

    system_message_content = (
        "You are an expert at finding fun activities for toddlers in Bengaluru. "
        "Your goal is to find one single, real, and suitable activity based on the user's preferences. "
        "You MUST use the 'web_search' tool to find information. "
        "After getting the search results, pick the best activity and return ONLY its name and address as a JSON object. "
        "Do not include any other text, explanation, or markdown formatting. "
        "Example: {\"name\": \"Cubbon Park\", \"address\": \"Kasturba Road, Bengaluru\"}"
    )

    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content=system_message_content),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
        HumanMessagePromptTemplate.from_template("{input}"),
    ])
    
    tools = [web_search]
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=50, handle_parsing_errors=True)

    input_string = (
        f"Please find an activity for a child in the '{child_age}' age range. "
        f"They prefer these types of activities: {', '.join(activity_types)}."
    )

    try:
        response = agent_executor.invoke({
            "input": input_string,
        })
        
        response_str = response.get("output", "")
        print(f"Raw AgentExecutor Output: {response_str}") # Debug print
        
        activity = json.loads(response_str)
        print(f"Found activity: {activity}")
        return {"activity": activity}

    except (json.JSONDecodeError, TypeError) as e:
        print(f"Error parsing activity JSON from agent output: {e}")
        return {"activity": None}
    except Exception as e:
        print(f"An unexpected error occurred in find_activity: {e}")
        return {"activity": None}
