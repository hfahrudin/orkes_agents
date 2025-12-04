import json
from typing import TypedDict
from orkes.graph.core import OrkesGraph
from orkes.agents.core import Agent
from orkes.services.prompts import ChatPromptHandler
from orkes.services.responses import ChatResponse
from orkes_agents.utils import AgentInterface

from orkes_agents.food_recommender.state import State
from orkes_agents.food_recommender.prompt import planner_prompt_system, planner_prompt_input, final_recommendation_prompt_system, final_recommendation_prompt_input
from orkes_agents.food_recommender.utils import get_current_location, duckduckgo_search

import re

def extract_json(raw_text):
    """
    Extract and parse JSON from a string that may contain
    markdown code fences or extra characters.
    
    Args:
        raw_text (str): Input string containing JSON.
        
    Returns:
        dict: Parsed JSON object.
    """
    # Remove markdown code fences if present
    cleaned = re.sub(r"```json\s*|```", "", raw_text, flags=re.IGNORECASE).strip()
    
    # Parse the cleaned JSON string
    return json.loads(cleaned)

class FoodRecommenderAgent(AgentInterface):
    def __init__(self, llm_engine, task_input):
        self.llm_engine = llm_engine
        self.task_input = task_input
        self.graph = OrkesGraph(State)
        self._build_graph()

    def planner_node(self, state: State):
        cP = ChatPromptHandler(
            system_prompt_template=planner_prompt_system,
            user_prompt_template=planner_prompt_input
        )
        agent = Agent("planner", cP, self.llm_engine, ChatResponse())
        
        # Provide current location to the planner
        location = state.get("location", "unknown")
        
        raw = agent.invoke(queries={"user": {"query": state['query'], "location": location}})["choices"][0]["message"]["content"]
        state["plan"] = extract_json(raw)
        return state

    def action_node(self, state: State):
        tool_results = []
        for p in state["plan"]:
            if p["agent"] == "get_current_location":
                result = get_current_location()
                state["location"] = result
                tool_results.append({"tool": "get_current_location", "result": result})
            elif p["agent"] == "duckduckgo_search":
                query_with_location = p["task"]["query"].format(location=state.get("location", "unknown"))
                result = duckduckgo_search(query_with_location)
                state["search_results"].extend(result)
                tool_results.append({"tool": "duckduckgo_search", "query": query_with_location, "result": result})
        return state

    def exit_node(self, state: State):
        cP = ChatPromptHandler(
            system_prompt_template=final_recommendation_prompt_system,
            user_prompt_template=final_recommendation_prompt_input
        )
        agent = Agent("recommender", cP, self.llm_engine, ChatResponse())
        raw = agent.invoke(queries={"user": {"search_results": json.dumps(state["search_results"])}})["choices"][0]["message"]["content"]
        state["final_recommendation"] = raw
        return state

    def _build_graph(self):
        START = self.graph.START
        END = self.graph.END

        self.graph.add_node('planner_node', self.planner_node)
        self.graph.add_node('action_node', self.action_node)
        self.graph.add_node('exit_node', self.exit_node)

        self.graph.add_edge(START, 'planner_node')
        self.graph.add_edge('planner_node', 'action_node')
        self.graph.add_edge('action_node', 'exit_node')
        self.graph.add_edge('exit_node', END)

        self.runner = self.graph.compile()

    def run(self):
        state = {
            "query": self.task_input.get("query", ""),
            "location": "",
            "search_results": [],
            "final_recommendation": "",
            "plan": []
        }
        result = self.runner.run(state)
        print(json.dumps(result, indent=2))
