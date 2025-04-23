import asyncio
from typing import AsyncGenerator, List
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import box
from rich.table import Table

from utils.events import (
    AgentEvent, UserQueryEvent, AgentResponseEvent, ToolCallEvent,
    FinalResponseEvent, ConversationStartEvent, ConversationEndEvent, ErrorEvent
)

# Initialize Rich console
console = Console()

def print_agent_instructions(instructions: str) -> None:
    """Print the agent instructions using Rich formatting.
    
    Args:
        instructions: The combined instructions for the agent
    """
    console.print()
    # Create a table for instructions with padding
    instructions_table = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
    instructions_table.add_column("Instructions")
    instructions_table.add_row(instructions)
    
    console.print(Panel(
        instructions_table,
        title="📋 AGENT INSTRUCTIONS",
        title_align="left",
        border_style="blue",
        box=box.ROUNDED,
        width=100,
        expand=False
    ))
    console.print()

def print_agent_info(agent_name: str, model_name: str, tools_count: int, target: str) -> None:
    """Print information about the created agent using Rich formatting.
    
    Args:
        agent_name: Name of the agent
        model_name: Name of the model used
        tools_count: Number of tools available
        target: Target platform (android, ios, or web)
    """
    # Format agent creation debug output with Rich
    agent_info = Text()
    agent_info.append("🤖 ", style="bold")
    agent_info.append(f"Agent '", style="dim")
    agent_info.append(f"{agent_name}", style="cyan bold")
    agent_info.append(f"' created using model '", style="dim")
    agent_info.append(f"{model_name}", style="green")
    agent_info.append(f"' with ", style="dim")
    agent_info.append(f"{tools_count}", style="yellow bold")
    agent_info.append(" tools from MCP server.", style="dim")
    
    platform_info = Text()
    platform_info.append("🎯 ", style="bold")
    platform_info.append("Target platform: ", style="dim")
    platform_info.append(f"{target}", style="magenta bold")
    
    console.print(agent_info)
    console.print(platform_info)
    console.print()

async def print_agent_events(event_generator: AsyncGenerator[AgentEvent, None]):
    """Consume agent events and print them using Rich formatting."""
    async for event in event_generator:
        if isinstance(event, ConversationStartEvent):
            console.rule("[bold blue]New Conversation", style="blue")
        
        elif isinstance(event, UserQueryEvent):
            # Create a table for user query with padding
            user_table = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
            user_table.add_column("Query")
            user_table.add_row(event.query)
            
            console.print(Panel(
                user_table, 
                title="🧑 USER QUERY",
                title_align="left",
                box=box.ROUNDED, 
                border_style="cyan", 
                expand=False, 
                width=100
            ))
        
        elif isinstance(event, AgentResponseEvent):
            # Truncate text to remove empty lines at the end
            truncated_text = event.text.rstrip()
            
            # Create a table for agent response with padding
            agent_table = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
            agent_table.add_column("Response")
            agent_table.add_row(truncated_text)
            
            console.print(Panel(
                agent_table,
                title="🤖 AGENT",
                title_align="left",
                border_style="yellow",
                box=box.ROUNDED,
                width=100,
                expand=False
            ))
        
        elif isinstance(event, ToolCallEvent):
            # Create a table for tool details
            tool_table = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
            tool_table.add_column("Property", style="green")
            tool_table.add_column("Value")
            
            tool_table.add_row("Function", event.name)
            tool_table.add_row("Arguments", str(event.args))
            
            console.print(Panel(
                tool_table,
                title="🔧 TOOL",
                title_align="left",
                border_style="green",
                box=box.ROUNDED,
                width=100,
                expand=False
            ))
        
        elif isinstance(event, FinalResponseEvent):
            # Truncate final response text to remove empty lines at the end
            truncated_text = event.text.rstrip()
            
            # Create a table for final response with padding
            final_table = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
            final_table.add_column("Response")
            final_table.add_row(f"📝 {truncated_text}")
            
            console.print(Panel(
                final_table,
                title="🎯 FINAL RESPONSE",
                title_align="left",
                border_style="magenta",
                box=box.ROUNDED,
                width=100,
                expand=False
            ))
        
        elif isinstance(event, ErrorEvent):
            console.print(Panel(
                f"❌ Error: {event.message}",
                title="ERROR",
                title_align="left",
                border_style="red",
                box=box.ROUNDED,
                width=100,
                expand=False
            ))
        
        elif isinstance(event, ConversationEndEvent):
            console.rule("[bold blue]End of Conversation", style="blue")