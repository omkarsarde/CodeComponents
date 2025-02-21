"""Environment variable loading and validation."""
import os
from pathlib import Path
from typing import Dict, Optional
from dotenv import load_dotenv, find_dotenv

class EnvironmentError(Exception):
    """Custom exception for environment-related errors."""
    pass

def load_env() -> Dict[str, str]:
    """Load and validate environment variables.
    
    Returns:
        Dict[str, str]: Dictionary containing validated environment variables
        
    Raises:
        EnvironmentError: If required variables are missing or invalid
    """
    # Find .env file, looking in parent directories if not in current
    env_path = find_dotenv(usecwd=True)
    if not env_path:
        raise EnvironmentError(
            "No .env file found. Please create one with required variables:\n"
            "OPENAI_API_KEY=your_key_here\n"
            "OPENAI_MODEL_NAME=gpt-4\n"
            "TEMPERATURE=0.7"
        )
    
    # Load the .env file
    load_dotenv(env_path)
    
    # Required environment variables with their descriptions
    required_vars = {
        "OPENAI_API_KEY": "Your OpenAI API key",
        "OPENAI_MODEL_NAME": "The OpenAI model to use (default: gpt-4)",
    }
    
    # Optional variables with default values
    optional_vars = {
        "TEMPERATURE": "0.7",
    }
    
    # Check for required variables
    missing_vars = []
    for var, description in required_vars.items():
        if not os.getenv(var):
            missing_vars.append(f"{var} ({description})")
    
    if missing_vars:
        raise EnvironmentError(
            "Missing required environment variables:\n" + 
            "\n".join(f"- {var}" for var in missing_vars)
        )
    
    # Build config with all variables
    config = {
        key.lower(): os.getenv(key)
        for key in required_vars.keys()
    }
    
    # Add optional variables with defaults
    for key, default in optional_vars.items():
        config[key.lower()] = os.getenv(key, default)
    
    return config

def get_env_var(name: str, default: Optional[str] = None) -> str:
    """Get a specific environment variable with optional default.
    
    Args:
        name: Name of the environment variable
        default: Optional default value if variable is not set
        
    Returns:
        str: The value of the environment variable
        
    Raises:
        EnvironmentError: If the variable is not found and no default is provided
    """
    value = os.getenv(name, default)
    if value is None:
        raise EnvironmentError(
            f"Environment variable {name} not found and no default provided"
        )
    return value 