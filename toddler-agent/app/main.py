from fastapi import FastAPI

app = FastAPI(
    title="Toddler Activity Planner API",
    description="An API for planning toddler-friendly weekend activities in Bengaluru.",
    version="0.1.0",
)

@app.get("/")
def read_root():
    """A simple endpoint to confirm the API is running."""
    return {"message": "Welcome to the Toddler Activity Planner API"}
