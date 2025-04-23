from google.adk.agents import Agent
from utils.tools import get_tools_async
from utils.display import print_agent_instructions, print_agent_info
from pathlib import Path
import sys

def load_instruction(target=None):
    """Load the agent instruction from a file.
    
    Args:
        target: The target platform (android, ios, or web)
    """
    instruction_path = Path(__file__).parent.parent / "prompts" / "agent_instruction.txt"
    
    if not instruction_path.exists():
        print(f"Error: Base instruction file {instruction_path} not found. Cannot proceed.", file=sys.stderr)
        sys.exit(1)
    
    with open(instruction_path, 'r') as f:
        instruction = f.read().strip()
    
    # Append target-specific instructions if available
    if target:
        # For android/ios, first load the general mobile instructions
        if target in ["android", "ios"]:
            mobile_instruction_path = Path(__file__).parent.parent / "prompts" / "mobile_instruction.txt"
            if mobile_instruction_path.exists():
                with open(mobile_instruction_path, 'r') as f:
                    mobile_instruction = f.read().strip()
                instruction = f"{instruction}\n\n{mobile_instruction}"
            else:
                print(f"Warning: {mobile_instruction_path} not found. Using base instruction only.")
        
        # Then load target-specific instructions
        target_instruction_path = Path(__file__).parent.parent / "prompts" / f"{target}_instruction.txt"
        if target_instruction_path.exists():
            with open(target_instruction_path, 'r') as f:
                target_instruction = f.read().strip()
            instruction = f"{instruction}\n\n{target_instruction}"
        else:
            print(f"Warning: {target_instruction_path} not found. Using base instruction only.")
    
    # Final strip to ensure no trailing empty lines
    instruction = instruction.strip()
    
    return instruction

async def get_agent_async(model_name, target):
    """Creates an ADK Agent equipped with tools from the MCP Server.
    
    Args:
        model_name: The name of the model to use
        target: The target platform (android, ios, or web)
    """
    # Get the appropriate tools based on the target
    tools, exit_stack = await get_tools_async(target)
    
    # Load instruction from file with the target platform
    instruction = load_instruction(target)
    
    # Print the combined instructions using the dedicated display function
    print_agent_instructions(instruction)
    
    # Create the agent
    root_agent = Agent(
        name="uitesting_agent_v1",
        model=model_name,
        description="Provide UI testing services",
        instruction=instruction,
        tools=tools,
    )
    
    # Print agent information using the dedicated display function
    print_agent_info(root_agent.name, model_name, len(tools), target)
    
    return root_agent, exit_stack