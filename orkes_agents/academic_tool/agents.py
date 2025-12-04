
import pickle
import copy
import json
from typing import TypedDict
from orkes.graph.core import OrkesGraph
from orkes.agents.core import Agent
from orkes.services.prompts import ChatPromptHandler
from orkes.services.responses import ChatResponse
from orkes_agents.utils import AgentInterface
from orkes_agents.academic_tool.prompt import system_prompt, user_prompt
from orkes_agents.academic_tool.state import State
import re

# This is a placeholder for the log_path decorator.
def log_path(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

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

class academia_toolkits:
    # init
    def __init__(self, path, dataset):
        self.paper_net = None
        self.author_net = None
        self.id2title_dict = None
        self.title2id_dict = None
        self.id2author_dict = None
        self.author2id_dict = None
        self.path = path
        self.dataset = dataset
        self.load_graph('dblp')


    def load_graph(self, graph_name):
        # print(graph_name)       
        if graph_name == 'dblp' or graph_name == "DBLP":
            # Load empty pickle files
            with open('{}/data/tool-query/academia/raw/paper_net.pkl'.format(self.path), 'rb') as f:
                self.paper_net = pickle.load(f) if f.read(1) else None

            with open('{}/data/tool-query/academia/raw/author_net.pkl'.format(self.path), 'rb') as f:
                self.author_net = pickle.load(f) if f.read(1) else None
            
            with open("{}/data/tool-query/academia/raw/title2id_dict.pkl".format(self.path), "rb") as f:
                self.title2id_dict = pickle.load(f) if f.read(1) else {}
            with open("{}/data/tool-query/academia/raw/author2id_dict.pkl".format(self.path), "rb") as f:
                self.author2id_dict = pickle.load(f) if f.read(1) else {}
            with open("{}/data/tool-query/academia/raw/id2title_dict.pkl".format(self.path), "rb") as f:
                self.id2title_dict = pickle.load(f) if f.read(1) else {}
            with open("{}/data/tool-query/academia/raw/id2author_dict.pkl".format(self.path), "rb") as f:
                self.id2author_dict = pickle.load(f) if f.read(1) else {}
            return True, "DBLP data is loaded, including two sub-graphs: AuthorNet and PaperNet."
        else:
            return False, "{} is not a valid graph name.".format(graph_name)
    
    @log_path
    def neighbourCheck(self, graph, node):
        return True, ["Not implemented yet"]
    
    @log_path
    def paperNodeCheck(self, node=None):
        return True, "Not implemented yet"
    
    @log_path
    def authorNodeCheck(self, node=None):
        return True, "Not implemented yet"

    def check_nodes(self, graph, node):
        return True, "Not implemented yet"

    @log_path
    def authorEdgeCheck(self, node1=None, node2=None):
        return True, "Not implemented yet"
    
    @log_path
    def paperEdgeCheck(self, node1=None, node2=None):
        return True, "Not implemented yet"

    def check_edges(self, graph, node1, node2):
        return True, "Not implemented yet"
        
    @log_path
    def finish(self, answer):
        if type(answer) == list:
            answer = sorted(answer)
        return True, answer

class AcademicToolAgent(AgentInterface):
    def __init__(self, llm_interface, task_input):
        self.llm_interface = llm_interface
        self.task_input = task_input
        self.graph = OrkesGraph(State)
        self.tool_kit = academia_toolkits(path=".", dataset="dblp")
        self._build_graph()

    def planner_node(self, state: State):
        cP = ChatPromptHandler(
            system_prompt_template=system_prompt,
            user_prompt_template=user_prompt
        )
        agent = Agent("planner", cP, self.llm_interface, ChatResponse())
        raw = agent.invoke(queries={"user": {"query": state['query']}})["choices"][0]["message"]["content"]
        state["plan"] = extract_json(raw)
        return state
    
    def action_node(self, state: State):
        results = []
        for p in state["plan"]:
            tool_to_call = getattr(self.tool_kit, p["agent"])
            result = tool_to_call(**p["task"])
            results.append(result)
        state['answer'] = json.dumps(results)
        return state
        
    def exit_node(self, state: State):
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
            "plan": [],
            "answer": ""
        }
        result = self.runner.run(state)
        print(json.dumps(result, indent=2))
