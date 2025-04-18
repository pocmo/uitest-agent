import asyncio
import warnings
import logging
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# Import from our new modular structure
from utils.config import setup_environment, get_default_model
from utils.agent import get_agent_async
from utils.cli import parse_args

warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.ERROR)

# Load configuration and setup environment
config = setup_environment()
DEFAULT_MODEL = get_default_model(config)

async def async_main():
    args = parse_args()
    
    model_to_use = args.model if args.model else DEFAULT_MODEL
    
    session_service = InMemorySessionService()

    # Define constants for identifying the interaction context
    APP_NAME = "ui-test-agent"
    USER_ID = "user_1"
    SESSION_ID = "session_001" # Using a fixed ID for simplicity

    session_service.create_session(
        state={}, app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )

    root_agent, exit_stack = await get_agent_async(model_to_use)

    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service
    )

    async def call_agent_async(query: str):
        """Sends a query to the agent and prints the final response."""
        print(f"\n>>> User Query: {query}")

        content = types.Content(role='user', parts=[types.Part(text=query)])

        final_response_text = "Agent did not produce a final response."

        async for event in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=content):
            if event.is_final_response():
                if event.content and event.content.parts:
                    final_response_text = event.content.parts[0].text
                elif event.actions and event.actions.escalate: # Handle potential errors/escalations
                    final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
                break

        print(f"<<< Agent Response: {final_response_text}")

    await call_agent_async(args.query)
    await exit_stack.aclose()

if __name__ == "__main__":
    asyncio.run(async_main())
