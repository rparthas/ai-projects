from langchain.tools import tool
from ddgs import DDGS

@tool
def web_search(query: str) -> str:
    """Performs a web search using DuckDuckGo for the given query and returns the top 3 results.
    Use this to find activities, restaurants, or other information on the web.
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
            if not results:
                return "No results found."
            
            # Format the results into a single string
            return "\n".join([f"- {r['title']}: {r['body']}" for r in results])

    except Exception as e:
        return f"Error performing web search: {e}"
