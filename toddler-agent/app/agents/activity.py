# This file will contain the logic for the Activity Agent node.

def find_activity(state: dict) -> dict:
    """Finds an activity and updates the state."""
    print("---NODE: Finding Activity---")
    # In the future, this will use an LLM and the search tool.
    activity = {
        "name": "Cubbon Park",
        "address": "Kasturba Road, Bengaluru"
    }
    return {"activity": activity}
