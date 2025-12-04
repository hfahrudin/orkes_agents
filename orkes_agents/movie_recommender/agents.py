from orkes.graph.core import OrkesGraph
from orkes.agents.core import Agent
from orkes.services.prompts import ChatPromptHandler
from orkes.services.responses import ChatResponse

from orkes_agents.movie_recommender.utils import *
from orkes_agents.movie_recommender.prompt import *
from orkes_agents.movie_recommender.state import State

from orkes_agents.utils import AgentInterface

class MovieRecommenderAgent(AgentInterface):
    def __init__(self, llm_engine, task_input):
        self.llm_engine = llm_engine
        self.graph = OrkesGraph(State)
        self.task_input = task_input
        self._build_graph()

    def planner_node(self, state: State):
        cR = ChatResponse()
        cP = ChatPromptHandler(
            system_prompt_template=planner_prompt_system,
            user_prompt_template=planner_prompt_input
        )

        queries = {
            "system": {
                "genre": state["user_profile"]["favorite_genres"],
                "watched_anime": state["user_profile"]["watched_anime"],
                "preferred_length": state["user_profile"]["preferred_length"],
                "query": state["query"],
            }
        }

        agent = Agent("planner", cP, self.llm_engine, cR)
        raw = agent.invoke(queries=queries)["choices"][0]["message"]["content"]
        state["plan"] = extract_json(raw)
        return state

    def search_engine_agent(self, task, feedback):
        cR = ChatResponse()
        cP = ChatPromptHandler(
            system_prompt_template=action_prompt_system,
            user_prompt_template=action_prompt_input
        )

        agent = Agent("search_agent", cP, self.llm_engine, cR)
        raw = agent.invoke(queries={"user": {"task": task, "feedback": feedback}})["choices"][0]["message"]["content"]
        cleaned = extract_json(raw)

        query = cleaned["query"]
        results = search(query)
        return query, results

    def action_node(self, state: State):
        for p in state["plan"]:
            if p["agent"] == "SearchEngine":
                query, results = self.search_engine_agent(p["task"], state["feedback"])
                state["search_results"].append({
                    "task": p["task"],
                    "query": query,
                    "search_result": results
                })
        return state

    def eval_node(self, state: State):
        cR = ChatResponse()
        cP = ChatPromptHandler(
            system_prompt_template=eval_prompt_system,
            user_prompt_template=eval_prompt_input
        )

        agent = Agent("eval_agent", cP, self.llm_engine, cR)
        raw = agent.invoke(queries={"user": {"results": state["search_results"]}})["choices"][0]["message"]["content"]
        cleaned = extract_json(raw)

        if cleaned["need_additional_search"]:
            state["status"] = "RETRY"
            state["feedback"] = cleaned["feedback"]
        else:
            state["status"] = "DONE"

        return state

    def conditional_node(self, state: State):
        return "DONE" if state["status"] == "DONE" else "RETRY"

    def exit_node(self, state: State):
        cR = ChatResponse()
        cP = ChatPromptHandler(
            system_prompt_template=final_recom_prompt_system,
            user_prompt_template=final_recom_input
        )

        agent = Agent("final_agent", cP, self.llm_engine, cR)
        raw = agent.invoke(queries={"user": {"results": state["search_results"]}})["choices"][0]["message"]["content"]

        state["final_recommendations"] = extract_json(raw)
        return state


    def _build_graph(self):
        START = self.graph.START
        END = self.graph.END

        self.graph.add_node("planner_node", self.planner_node)
        self.graph.add_node("action_node", self.action_node)
        self.graph.add_node("eval_node", self.eval_node)
        self.graph.add_node("exit_node", self.exit_node)

        self.graph.add_edge(START, "planner_node")
        self.graph.add_edge("planner_node", "action_node")
        self.graph.add_edge("action_node", "eval_node")

        self.graph.add_conditional_edge(
            "eval_node",
            self.conditional_node,
            {"DONE": "exit_node", "RETRY": "action_node"}
        )

        self.graph.add_edge("exit_node", END)

        self.runner = self.graph.compile()


    def run(self):
        task_input = self.task_input
        query = task_input['query']
        user_profile = task_input['user_profile']
        state: State = {
            "query": query,
            "user_profile": user_profile,
            "search_results": [],
            "final_recommendations": [],
            "feedback": "",
            "plan": [],
            "status": "DONE"
        }

        return self.runner.run(state)
