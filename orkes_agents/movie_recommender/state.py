from typing import TypedDict
class State(TypedDict):
    query: str
    user_profile: dict
    search_results: list
    final_recommendations: list
    feedback: str
    plan: list
    status: str