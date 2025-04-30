from typing import AsyncGenerator
from google.adk.runners import Runner
from google.genai import types

from utils.events import (
    AgentEvent, UserQueryEvent, AgentResponseEvent, ToolCallEvent,
    FinalResponseEvent, ConversationStartEvent, ConversationEndEvent, ErrorEvent,
    ToolResponseEvent
)

async def process_agent_interaction(
    runner: Runner, 
    query: str, 
    user_id: str, 
    session_id: str
) -> AsyncGenerator[AgentEvent, None]:
    """Process agent interaction and yield structured event objects.
    
    Args:
        runner: The agent runner instance
        query: The user's query text
        user_id: ID of the current user
        session_id: Current session ID
        
    Yields:
        AgentEvent objects representing the conversation flow
    """
    # Start conversation
    yield ConversationStartEvent()
    
    # Yield the user query event
    yield UserQueryEvent(query)
    
    # Set up content for the agent
    content = types.Content(role='user', parts=[types.Part(text=query)])
    
    # Process agent's response
    try:
        async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
            # Check if this is a final response first
            is_final = event.is_final_response()
            
            # Process intermediate agent responses (only if not a final response)
            if not is_final and event.content and event.content.parts:
                intermediate_text = event.content.parts[0].text
                if intermediate_text:  # Skip None or empty text
                    yield AgentResponseEvent(intermediate_text)
            
            # Process tool calls
            function_calls = event.get_function_calls() if hasattr(event, 'get_function_calls') else []
            for call in function_calls:
                yield ToolCallEvent(call.name, call.args)

            # Process function responses
            function_responses = event.get_function_responses() if hasattr(event, 'get_function_responses') else []
            for response in function_responses:
                yield ToolResponseEvent(response.name, response.response)
            
            # Handle final response
            if is_final:
                if event.content and event.content.parts:
                    final_response_text = event.content.parts[0].text
                elif event.actions and event.actions.escalate:
                    final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
                else:
                    final_response_text = "Agent did not produce a final response."
                
                yield FinalResponseEvent(final_response_text)
    except Exception as e:
        yield ErrorEvent(str(e))
    
    # End conversation
    yield ConversationEndEvent()