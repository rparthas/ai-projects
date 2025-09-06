from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

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

class Activity(BaseModel):
    name: str = Field(..., description="Name of the activity")
    location: str = Field(..., description="Location of the activity")
    description: str = Field(..., description="Description of the activity")
    estimated_cost: str = Field(..., description="Estimated cost")
    duration: str = Field(..., description="Estimated duration")
    age_appropriate: bool = Field(..., description="Whether it's age appropriate")
    activity_type: ActivityType = Field(..., description="Type of activity")

class WeekendPlan(BaseModel):
    activities: List[Activity] = Field(..., description="List of recommended activities")
    total_estimated_cost: str = Field(..., description="Total estimated cost for all activities")
    additional_tips: List[str] = Field(..., description="Additional tips for the weekend")

app = FastAPI(
    title="Toddler Activity Planner API",
    description="An API for planning toddler-friendly weekend activities in Bengaluru.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    """A simple endpoint to confirm the API is running."""
    return {"message": "Welcome to the Toddler Activity Planner API"}

@app.post("/plan-weekend", response_model=WeekendPlan)
def plan_weekend(preferences: UserPreferences):
    """
    Generate a weekend activity plan based on user preferences.
    
    This endpoint accepts user preferences and returns a personalized
    weekend activity plan for toddlers in Bengaluru.
    """
    sample_activities = [
        Activity(
            name="Lalbagh Botanical Garden",
            location="Lalbagh, Bengaluru",
            description="Beautiful botanical garden perfect for morning walks with toddlers",
            estimated_cost="₹10-20 per person",
            duration="2-3 hours",
            age_appropriate=True,
            activity_type=ActivityType.OUTDOOR
        ),
        Activity(
            name="Cubbon Park",
            location="Cubbon Park, Bengaluru",
            description="Large park with plenty of space for kids to run around",
            estimated_cost="Free",
            duration="1-2 hours",
            age_appropriate=True,
            activity_type=ActivityType.OUTDOOR
        )
    ]
    
    return WeekendPlan(
        activities=sample_activities,
        total_estimated_cost="₹20-40",
        additional_tips=[
            "Carry water and snacks for the little one",
            "Best to visit parks in the morning or evening",
            "Don't forget sun protection and comfortable shoes"
        ]
    )
