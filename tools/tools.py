from langchain_community.tools.tavily_search import TavilySearchResults

# using TavilySearch to connect LLM to the web


def get_profile_url_tavily(name: str):
    """Searches for Linkedin or Twitter Profile Page"""

    # init the Tavily object
    search = TavilySearchResults()
    # same response as how it was run in the api playground
    res = search.run(f"{name}")

    return res
