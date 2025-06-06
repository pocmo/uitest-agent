import asyncio
import warnings
import logging
import uuid
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from rich.console import Console

# Import from our modular structure
from utils.config import setup_environment, get_default_model, use_litellm
from utils.agent import get_agent_async
from utils.cli import parse_args
from utils.display import print_agent_events
from utils.interactions import process_agent_interaction

# Suppress warnings and reduce logging noise for cleaner output
warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.ERROR)

# Load configuration and setup environment
config = setup_environment()
DEFAULT_MODEL = get_default_model(config)
USE_LITELLM = use_litellm(config)

# Initialize Rich console
console = Console()

async def async_main():
    args = parse_args()
    
    model_to_use = args.model if args.model else DEFAULT_MODEL
    target = args.target
    
    session_service = InMemorySessionService()

    # Define app name and generate random session ID
    APP_NAME = "ui-test-agent"
    USER_ID = "user"
    SESSION_ID = str(uuid.uuid4())

    session_service.create_session(
        state={}, app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )

    root_agent, exit_stack = await get_agent_async(model_to_use, target, USE_LITELLM)

    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service
    )

    # Process and print agent events
    event_generator = process_agent_interaction(
        runner=runner,
        query=args.query,
        user_id=USER_ID,
        session_id=SESSION_ID
    )
    await print_agent_events(event_generator)
    await exit_stack.aclose()

if __name__ == "__main__":
    asyncio.run(async_main())
