import os
import yaml
from pathlib import Path

def load_config():
    """Load configuration from config.yaml file."""
    config_path = Path(__file__).parent.parent / "config.yaml"
    if not config_path.exists():
        print("No config.yaml found. See config.sample.yaml for reference and create your own config.yaml.")
        return {}
        
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def setup_environment():
    """Set up environment variables from config."""
    config = load_config()
    
    # Check for API key in config or environment
    if not config.get('google_api_key') and not os.environ.get('GOOGLE_API_KEY'):
        print("Warning: No Google API key found. Set in config.yaml or as GOOGLE_API_KEY environment variable.")
    
    # Set environment variables from config if provided
    if 'google_api_key' in config:
        os.environ["GOOGLE_API_KEY"] = config.get('google_api_key')
    if 'use_vertex_ai' in config:
        os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = str(config.get('use_vertex_ai')).lower()
    
    return config

def get_default_model(config):
    """Get the default model name from config."""
    return config.get('model_name', "gemini-2.5-pro-preview-03-25")

def use_litellm(config):
    """Check if LiteLLM should be used based on config."""
    return config.get('use_litellm', False)