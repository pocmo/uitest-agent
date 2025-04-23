import asyncio
from typing import AsyncGenerator
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
# Dictionary to store header print state
header_flags = {"agent_header_printed": False, "tool_header_printed": False}

async def print_agent_events(event_generator: AsyncGenerator[AgentEvent, None]):
    """Consume agent events and print them using Rich formatting."""
    async for event in event_generator:
        if isinstance(event, ConversationStartEvent):
            console.rule("[bold blue]New Conversation", style="blue")
        
        elif isinstance(event, UserQueryEvent):
            user_text = Text("🧑 USER QUERY", style="bold cyan")
            console.print(user_text)
            console.print(Panel(
                f"💬 {event.query}", 
                box=box.ROUNDED, 
                border_style="cyan", 
                expand=False, 
                width=100
            ))
        
        elif isinstance(event, AgentResponseEvent):
            if not header_flags["agent_header_printed"]:
                agent_header = Text("🤖 AGENT PROCESSING", style="bold yellow")
                console.print(agent_header)
                header_flags["agent_header_printed"] = True
            
            console.print(Panel(
                f"🤖 {event.text}", 
                border_style="yellow",
                box=box.ROUNDED,
                width=100,
                expand=False
            ))
        
        elif isinstance(event, ToolCallEvent):
            if not header_flags["tool_header_printed"]:
                tool_header = Text("🔧 TOOL CALLS", style="bold green")
                console.print(tool_header)
                header_flags["tool_header_printed"] = True
            
            # Create a table for tool details
            tool_table = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
            tool_table.add_column("Property", style="green")
            tool_table.add_column("Value")
            
            tool_table.add_row("Function", event.name)
            tool_table.add_row("Arguments", str(event.args))
            
            console.print(Panel(
                tool_table,
                title="🔧 Tool Call",
                border_style="green",
                box=box.ROUNDED,
                width=100,
                expand=False
            ))
        
        elif isinstance(event, FinalResponseEvent):
            # Reset header flags for the next conversation
            header_flags["agent_header_printed"] = False
            header_flags["tool_header_printed"] = False
            
            final_header = Text("🎯 FINAL RESPONSE", style="bold magenta")
            console.print(final_header)
            
            console.print(Panel(
                f"📝 {event.text}",
                border_style="magenta",
                box=box.ROUNDED,
                width=100,
                expand=False
            ))
        
        elif isinstance(event, ErrorEvent):
            console.print(Panel(
                f"❌ Error: {event.message}",
                border_style="red",
                box=box.ROUNDED,
                width=100,
                expand=False
            ))
        
        elif isinstance(event, ConversationEndEvent):
            console.rule("[bold blue]End of Conversation", style="blue")