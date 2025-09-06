import json
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage

from app.tools.search_tool import web_search
from app.core.llm import llm

def find_restaurant(state: dict) -> dict:
    """
    Finds a suitable restaurant near the activity using a tool-calling agent.
    """
    print("---NODE: Finding Real Restaurant---")
    activity = state.get("activity")
    # TODO: Get dietary preference from state once it's added
    dietary_preference = "vegetarian"

    if not activity:
        return {"restaurant": None}

    system_message_content = (
        "You are an expert at finding kid-friendly restaurants. "
        "Your goal is to find one single, real, and suitable restaurant that is near the chosen activity. "
        "You MUST use the 'web_search' tool. "
        "After getting the search results, pick the best restaurant and return ONLY its name and address as a JSON object. "
        "Do not include any other text, explanation, or markdown formatting. "
        "Example: {\"name\": \"Corner House\", \"address\": \"Residency Road, Bengaluru\"}"
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
        f"The activity is '{activity.get("name")}' at '{activity.get("address")}'. "
        f"Please find a '{dietary_preference}' restaurant nearby that is good for families with toddlers."
    )

    try:
        response = agent_executor.invoke({
            "input": input_string,
        })
        
        response_str = response.get("output", "")
        print(f"Raw AgentExecutor Output: {response_str}") # Debug print
        
        restaurant = json.loads(response_str)
        print(f"Found restaurant: {restaurant}")
        return {"restaurant": restaurant}

    except (json.JSONDecodeError, TypeError) as e:
        print(f"Error parsing restaurant JSON from agent output: {e}")
        return {"restaurant": None}
    except Exception as e:
        print(f"An unexpected error occurred in find_restaurant: {e}")
        return {"restaurant": None}
