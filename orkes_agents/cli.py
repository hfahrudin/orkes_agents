import argparse
from orkes_agents.utils import validate_api_keys
from pathlib import Path


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


    args = parser.parse_args()
    validate_api_keys()

    # TODO: continue to execution logic


if __name__ == "__main__":
    main()
