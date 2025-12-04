import argparse
from orkes_agents.utils import validate_api_keys, create_llm_engine, load_input_json, AgentInterface
from pathlib import Path
from orkes_agents.movie_recommender.agents import MovieRecommenderAgent
from orkes_agents.academic_tool.agents import AcademicToolAgent
from orkes_agents.food_recommender.agents import FoodRecommenderAgent


def main():
    parser = argparse.ArgumentParser(
        prog="orkes-agents",
        description=(
            "Agentic based tools with Orkes as backend"
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument("--agents", required=True, help="Agent module or pipeline name.")
    parser.add_argument("-i", "--input", required=True, help="Input text/file for agent.")

    parser.add_argument(
        "-o", "--output",
        default=str(Path.cwd() / "output.txt"),
        help="Output path for agent result. Defaults to ./output.txt in current directory."
    )
    parser.add_argument(
        "-l", "--log",
        default=str(Path.cwd() / "orkes.log"),
        help="Execution log path. Defaults to ./orkes.log"
    )

    args = parser.parse_args()
    validate_api_keys()


    llm_interface = create_llm_engine()

    task_input = load_input_json(args.input)

    task_name = args.agents

    agent: AgentInterface = None
    if task_name == "movie_recommendation":
        agent = MovieRecommenderAgent(llm_interface, task_input)
    elif task_name == "academic_tool":
        agent = AcademicToolAgent(llm_interface, task_input)
    elif task_name == "food_recommendation":
        agent = FoodRecommenderAgent(llm_interface, task_input)
    else:
        raise RuntimeError(
            "Unknown Agent/Task name"
        )
    agent.run()

if __name__ == "__main__":
    main()
