from dotenv import load_dotenv
import os
from pathlib import Path
from orkes.services.connections import vLLMConnection
import json
from abc import ABC, abstractmethod


class AgentInterface(ABC):
    @abstractmethod
    def run(self):
        """Send a message and receive the full response."""
        pass
    

def load_input_json(input_arg: str) -> dict:
    """
    Loads JSON input from either:
    - a file path (if file exists)
    - a raw inline JSON string

    Always returns a parsed dict.
    """
    p = Path(input_arg)
    try:
        if p.exists():
            return json.loads(p.read_text())
        else:
            # Treat input_arg as inline JSON
            return json.loads(input_arg)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON input. Error: {e}")

def validate_api_keys():
    """Load .env and verify the OpenAI provider key is available."""
    
    env_path = Path(".env")
    if env_path.exists():
        load_dotenv(env_path)
    else:
        print("[WARN] .env file not found — checking system environment variables only.")

    # Supported provider is now only OpenAI
    key_map = {
        "OpenAI": os.getenv("OPENAI_API_KEY"),
    }

    available = {provider: key for provider, key in key_map.items() if key}

    if not available:
        raise RuntimeError(
            "\nNo valid LLM credential detected.\n\n"
            "The runner requires the OpenAI key to operate.\n"
            "Set the following in your .env or environment:\n"
            "  • OPENAI_API_KEY\n"
        )

    print(f"🔑 Active Provider(s): {', '.join(available.keys())}")
    return available


def create_llm_engine():
    """
    Creates the LLM engine, supporting only OpenAI.
    """

    # Check only for the OpenAI key
    api_key = os.getenv("OPENAI_API_KEY")
    provider = "OpenAI"

    if not api_key:
        raise RuntimeError(
            f"No supported LLM provider API key found for {provider}. "
            "Set the OPENAI_API_KEY environment variable."
        )

    # Provider-specific model / URL defaults for OpenAI
    url = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
    # Updated default model to a commonly used, modern OpenAI model
    model_name = os.getenv("OPENAI_MODEL_NAME", "gpt-4.1")

    print(f"[INFO] Using provider: {provider} | Model: {model_name}")

    # Create connection
    return vLLMConnection(
        url=url,
        model_name=model_name,
        api_key=api_key
    )
