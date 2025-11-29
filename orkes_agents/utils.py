from dotenv import load_dotenv
import os
from pathlib import Path

def validate_api_keys():
    """Load .env and verify at least one LLM provider key is available."""
    
    env_path = Path(".env")
    if env_path.exists():
        load_dotenv(env_path)
    else:
        print("[WARN] .env file not found — checking system environment variables only.")

    # Supported providers
    key_map = {
        "OpenAI": os.getenv("OPENAI_API_KEY"),
        "Gemini": os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"),
        "Claude": os.getenv("ANTHROPIC_API_KEY") or os.getenv("CLAUDE_API_KEY"),
    }

    available = {provider: key for provider, key in key_map.items() if key}

    if not available:
        raise RuntimeError(
            "\ No valid LLM credential detected.\n\n"
            "The runner requires at least one provider key to operate.\n"
            "Set one of the following in your .env or environment:\n"
            "  • OPENAI_API_KEY\n"
            "  • GEMINI_API_KEY or GOOGLE_API_KEY\n"
            "  • ANTHROPIC_API_KEY or CLAUDE_API_KEY\n"
        )

    print(f"🔑 Active Provider(s): {', '.join(available.keys())}")
    return available
