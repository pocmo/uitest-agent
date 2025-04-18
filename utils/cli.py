import argparse

def parse_args():
    """Parse command line arguments for the UI Testing Agent."""
    parser = argparse.ArgumentParser(description="Run UI Testing Agent")
    parser.add_argument("--query", type=str, help="Query to send to the agent",
                    default="Take a screenshot of the currently running Android device and describe what you see.")
    parser.add_argument("--model", type=str, help="Model to use for the agent (overrides config file)",
                    default=None)
    return parser.parse_args()