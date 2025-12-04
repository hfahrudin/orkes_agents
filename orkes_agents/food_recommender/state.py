from typing import TypedDict

class State(TypedDict):
    query: str
    location: str
    search_results: list
    final_recommendation: str
    plan: list