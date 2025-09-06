# This file will contain the logic for the Restaurant Agent node.

def find_restaurant(state: dict) -> dict:
    """Finds a restaurant and updates the state."""
    print("---NODE: Finding Restaurant---")
    # In the future, this will use an LLM and the search tool.
    restaurant = {
        "name": "Corner House Ice Cream",
        "address": "Residency Road, Bengaluru"
    }
    return {"restaurant": restaurant}
