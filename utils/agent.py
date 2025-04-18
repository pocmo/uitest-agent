from google.adk.agents import Agent
from utils.tools import get_tools_async
from pathlib import Path

def load_instruction():
    """Load the agent instruction from a file."""
    instruction_path = Path(__file__).parent.parent / "prompts" / "agent_instruction.txt"
    
    if not instruction_path.exists():
        print(f"Warning: {instruction_path} not found. Using default instruction.")
        return "You are a mobile UI testing assistant."
    
    with open(instruction_path, 'r') as f:
        return f.read()

async def get_agent_async(model_name):
    """Creates an ADK Agent equipped with tools from the MCP Server."""
    tools, exit_stack = await get_tools_async()
    
    # Load instruction from file
    instruction = load_instruction()
    
    root_agent = Agent(
        name="uitesting_agent_v1",
        model=model_name,
        description="Provide UI testing services",
        instruction=instruction,
        tools=tools,
    )
    print(f"Agent '{root_agent.name}' created using model '{model_name}' with {len(tools)} tools from MCP server.")
    return root_agent, exit_stack