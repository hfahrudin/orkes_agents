from typing import TypedDict

class State(TypedDict):
    query: str
    plan: list
    answer: str
