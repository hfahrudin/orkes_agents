import argparse

def main():
    parser = argparse.ArgumentParser(
        description="Orkes_agents: Run agentic based tools"
    )
    parser.add_argument(
        "--agents",
        required=True,
        help="agent name"
    )
    parser.add_argument(
        "-i", "--input",
        required=True,
        help="agent input"
    )

    parser.add_argument(
        "-o", "--output",
        required=True,
        help="agent output"
    )

    parser.add_argument(
        "-l", "--log",
        required=True,
        help="loggin runner trace path"
    )
    args = parser.parse_args()
