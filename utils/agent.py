from google.adk.agents import Agent
from utils.tools import get_tools_async
from pathlib import Path
import sys

def load_instruction(target=None):
    """Load the agent instruction from a file.
    
    Args:
        target: The target platform (mobile or web)
    """
    instruction_path = Path(__file__).parent.parent / "prompts" / "agent_instruction.txt"
    
    if not instruction_path.exists():
        print(f"Error: Base instruction file {instruction_path} not found. Cannot proceed.", file=sys.stderr)
        sys.exit(1)
    
    with open(instruction_path, 'r') as f:
        instruction = f.read()
    
    # Append target-specific instructions if available
    if target:
        target_instruction_path = Path(__file__).parent.parent / "prompts" / f"{target}_instruction.txt"
        if target_instruction_path.exists():
            with open(target_instruction_path, 'r') as f:
                target_instruction = f.read()
            instruction = f"{instruction}\n\n{target_instruction}"
        else:
            print(f"Warning: {target_instruction_path} not found. Using base instruction only.")
    
    return instruction

async def get_agent_async(model_name, target="mobile"):
    """Creates an ADK Agent equipped with tools from the MCP Server.
    
    Args:
        model_name: The name of the model to use
        target: The target platform (mobile or web)
    """
    # Get the appropriate tools based on the target
    tools, exit_stack = await get_tools_async(target)
    
    # Load instruction from file with the target platform
    instruction = load_instruction(target)
    
    root_agent = Agent(
        name="uitesting_agent_v1",
        model=model_name,
        description="Provide UI testing services",
        instruction=instruction,
        tools=tools,
    )
    print(f"Agent '{root_agent.name}' created using model '{model_name}' with {len(tools)} tools from MCP server.")
    print(f"Agent target platform: {target}")
    return root_agent, exit_stack