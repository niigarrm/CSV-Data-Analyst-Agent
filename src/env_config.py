import os
from typing import Optional

from dotenv import load_dotenv


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
API_KEY_VAR = "ANTHROPIC_API_KEY"


# ---------------------------------------------------------------------------
# Environment loading
# ---------------------------------------------------------------------------
def load_environment() -> None:
    """
    Loads environment variables from a .env file in the project root into
    the process environment.

    This must be called once at application startup, before any other
    module attempts to read environment variables.

    If no .env file is found, python-dotenv fails silently — the function
    will not raise. In that case, any required variables must already be
    set in the actual process environment (e.g. via the shell), otherwise
    validate_api_key() will fail later.
    """
    load_dotenv()


# ---------------------------------------------------------------------------
# API key access
# ---------------------------------------------------------------------------
def get_api_key() -> Optional[str]:
    """
    Returns the ANTHROPIC_API_KEY value from the environment, or None if
    the variable is not set or is empty.

    Returns:
        The API key string, or None if the variable is missing or blank.
    """
    key = os.getenv(API_KEY_VAR)

    # Treat empty strings the same as missing keys
    if not key or not key.strip():
        return None

    return key


# ---------------------------------------------------------------------------
# Startup validation
# ---------------------------------------------------------------------------
def validate_api_key() -> bool:
    """
    Validates that the ANTHROPIC_API_KEY is set before the application
    attempts to call the Claude API.

    Prints a helpful setup message if the key is missing, so the user
    knows exactly what to do next.

    Returns:
        True if the key is present, False otherwise.
    """
    if get_api_key() is None:
        print(f"Error: {API_KEY_VAR} not found.")
        print("Please create a .env file in the project root with:")
        print(f"    {API_KEY_VAR}=your-key-here")
        print("You can get your key from: https://console.anthropic.com/")
        return False

    return True
