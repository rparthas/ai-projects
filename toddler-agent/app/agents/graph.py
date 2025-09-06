from typing import TypedDict, List, Optional
from langgraph.graph import StateGraph, END
from langchain_core.prompts import ChatPromptTemplate

from app.core.llm import llm
from app.agents.weather import get_weather
from app.agents.activity import find_activity
from app.agents.restaurant import find_restaurant

class PlanState(TypedDict):
    child_age: str
    activity_types: List[str]
    weather_info: Optional[str]
    activity: Optional[dict]
    restaurant: Optional[dict]
    final_plan: Optional[str]

def generate_plan_response(state: PlanState) -> dict:
    """
    Generates the final user-facing plan based on the gathered information.
    """
    print("---NODE: Generating Final Plan---")
    
    if not state.get("activity"):
        return {"final_plan": "I couldn't find a suitable activity based on your preferences. Please try again with different options."}

    prompt_template = (
        "You are a helpful assistant for parents. Based on the following information, create a fun, "
        "single-paragraph weekend plan for a toddler.\n\n"
        "Weather: {weather}\n"
        "Activity: {activity_name} at {activity_address}\n"
    )
    if state.get("restaurant"):
        prompt_template += "Restaurant: {restaurant_name} at {restaurant_address}\n\n"
    
    prompt_template += "Combine this into a friendly and appealing plan."

    prompt = ChatPromptTemplate.from_template(prompt_template)
    chain = prompt | llm
    
    plan = chain.invoke({
        "weather": state.get("weather_info"),
        "activity_name": state.get("activity", {}).get("name"),
        "activity_address": state.get("activity", {}).get("address"),
        "restaurant_name": state.get("restaurant", {}).get("name"),
        "restaurant_address": state.get("restaurant", {}).get("address"),
    })
    
    # Strip leading/trailing whitespace and quotes from the LLM's output
    clean_plan = plan.content.strip().strip('"')

    return {"final_plan": clean_plan}

def should_find_restaurant(state: PlanState) -> str:
    """
    Conditional edge: decides whether to search for a restaurant.
    """
    if state.get("activity"):
        return "find_restaurant"
    else:
        return "generate_plan"

workflow = StateGraph(PlanState)

workflow.add_node("get_weather", get_weather)
workflow.add_node("find_activity", find_activity)
workflow.add_node("find_restaurant", find_restaurant)
workflow.add_node("generate_plan", generate_plan_response)

workflow.set_entry_point("get_weather")
workflow.add_edge("get_weather", "find_activity")
workflow.add_conditional_edges(
    "find_activity",
    should_find_restaurant,
    {
        "find_restaurant": "find_restaurant",
        "generate_plan": "generate_plan",
    }
)
workflow.add_edge("find_restaurant", "generate_plan")
workflow.add_edge("generate_plan", END)

app_graph = workflow.compile()
