import os
import yaml
from pathlib import Path

def load_config():
    """Load configuration from config.yaml file."""
    config_path = Path(__file__).parent.parent / "config.yaml"
    if not config_path.exists():
        print(f"Warning: {config_path} not found. Using default values or environment variables.")
        return {}
        
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def setup_environment():
    """Set up environment variables from config."""
    config = load_config()
    
    os.environ["GOOGLE_API_KEY"] = config.get('google_api_key', os.environ.get('GOOGLE_API_KEY', ''))
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = str(config.get('use_vertex_ai', False)).lower()
    
    return config

def get_default_model(config):
    """Get the default model name from config."""
    return config.get('model_name', "gemini-2.5-pro-preview-03-25")