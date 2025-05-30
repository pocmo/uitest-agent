import asyncio
import pytest
from rich.console import Console

from utils.events import ToolResponseEvent
from utils.display import print_agent_events, console as display_console # Import the console used by the module

# Mock event generator
async def mock_event_generator_for_tool_response(event: ToolResponseEvent):
    yield event

@pytest.mark.asyncio
async def test_print_agent_events_tool_response_verbosity():
    """
    Tests that ToolResponseEvent is printed with correct verbosity
    based on the verbose flag.
    """
    original_console = display_console # Keep a reference to the original console
    
    # Mock ToolResponseEvent
    tool_name = "test_tool"
    tool_response_content = '{"output": "Test tool output details"}'
    event = ToolResponseEvent(name=tool_name, response=tool_response_content)
    
    # --- Test with verbose=True ---
    capturing_console_verbose = Console(record=True, width=100) # Rich console for capturing output
    # Patch the console in utils.display
    import utils.display
    utils.display.console = capturing_console_verbose

    await print_agent_events(mock_event_generator_for_tool_response(event), verbose=True)
    output_verbose = capturing_console_verbose.export_text()

    # Assertions for verbose output
    assert "↩️ TOOL RESPONSE" in output_verbose
    assert "Tool Name" in output_verbose
    assert tool_name in output_verbose
    assert "Response" in output_verbose # The field name
    assert tool_response_content in output_verbose # The actual content
    print(f"Verbose output:\n{output_verbose}") # For debugging in CI if needed

    # --- Test with verbose=False ---
    capturing_console_non_verbose = Console(record=True, width=100) # New console for this part
    utils.display.console = capturing_console_non_verbose # Patch again

    await print_agent_events(mock_event_generator_for_tool_response(event), verbose=False)
    output_non_verbose = capturing_console_non_verbose.export_text()

    # Assertions for non-verbose output
    assert "← Received response from tool" in output_non_verbose
    assert tool_name in output_non_verbose
    assert "↩️ TOOL RESPONSE" not in output_non_verbose # Panel title should not be there
    assert "Response" not in output_non_verbose # The field name for detailed view
    assert tool_response_content not in output_non_verbose # The detailed content
    print(f"Non-verbose output:\n{output_non_verbose}") # For debugging

    # Restore the original console
    utils.display.console = original_console

# Example of how to run this test with pytest (if pytest and pytest-asyncio are installed):
# Ensure you have:
# pytest
# pytest-asyncio
#
# Then run:
# pytest tests/test_display.py
