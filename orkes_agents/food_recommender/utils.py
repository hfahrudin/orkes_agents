from duckduckgo_search import DDGS

def get_current_location():
    """
    Simulates detecting the current location. In a real application, this would
    use a geolocation API or similar.
    For now, it returns a hardcoded location.
    """
    return "San Francisco, CA"

def duckduckgo_search(query, max_results=5):
    """
    Searches DuckDuckGo for the given query and returns the results.
    """
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results):
            results.append(r)
    return results