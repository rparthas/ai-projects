from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

from app.agents.graph import app_graph

# --- Enums and Models ---

class AgeRange(str, Enum):
    INFANT = "0-1"
    TODDLER = "1-3"
    PRESCHOOLER = "3-5"

class ActivityType(str, Enum):
    OUTDOOR = "outdoor"
    INDOOR = "indoor"
    EDUCATIONAL = "educational"
    RECREATIONAL = "recreational"
    CULTURAL = "cultural"

class UserPreferences(BaseModel):
    child_age: AgeRange = Field(..., description="Age range of the child")
    activity_types: List[ActivityType] = Field(..., description="Preferred types of activities")
    budget_range: str = Field(..., description="Budget range (e.g., 'low', 'medium', 'high')")
    transportation: str = Field(..., description="Available transportation mode")
    location_preference: Optional[str] = Field(None, description="Preferred area in Bengaluru")
    duration: str = Field(..., description="Available time duration")
    weather_preference: Optional[str] = Field(None, description="Weather preference if any")

class PlanResponse(BaseModel):
    plan: str

# --- FastAPI App ---

app = FastAPI(
    title="Toddler Activity Planner API",
    description="An API for planning toddler-friendly weekend activities in Bengaluru.",
    version="0.1.0",
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- API Endpoints ---

@app.get("/", response_class=FileResponse)
async def read_index():
    """Serves the index.html file from the static directory."""
    return "static/index.html"

@app.post("/plan-weekend", response_model=PlanResponse)
async def plan_weekend(preferences: UserPreferences):
    """
    Generate a weekend activity plan based on user preferences.
    """
    try:
        # Convert enums to strings for the graph state
        inputs = {
            "child_age": preferences.child_age.value,
            "activity_types": [at.value for at in preferences.activity_types],
        }
        
        # Invoke the agent graph
        final_state = app_graph.invoke(inputs)
        
        # Return the final plan
        plan_content = final_state.get("final_plan", "Could not generate a plan. Please check the server logs.")
        return PlanResponse(plan=plan_content)
    except Exception as e:
        print(f"!!! ERROR during graph execution: {e}") # Log the error to the console
        error_message = f"An error occurred on the server. This is likely due to the Ollama server not running or the model not being available. Error: {e}"
        return PlanResponse(plan=error_message)