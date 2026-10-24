"""
config.py - Central place for application settings.
 
Settings are read from environment variables, never hardcoded.
For local development, the variables are loaded from the .env file.
"""

import os

from dotenv import load_dotenv

# Read the .env file (if it exists) and add its values to the
# environment so os.getenv() can find them.
load_dotenv()

# Gemini API key. Returns None if the variable is not set.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Tavily API key, used for web search. Returns None if not set.
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# The placeholder text that ships in the .env file.
_TAVILY_PLACEHOLDER = "your_tavily_api_key_here"


def get_tavily_api_key():
    """Return the Tavily API key, or raise ValueError if it is missing.
 
    We check this ourselves because the Tavily SDK can run without a key
    in a limited "keyless" mode, which would hide a setup mistake.
    """
    key = (TAVILY_API_KEY or "").strip()

    if not key or key == _TAVILY_PLACEHOLDER:
        raise ValueError(
            "TAVILY_API_KEY is missing. Open the .env file and replace the "
            "placeholder with your Tavily API key (see README.md)."
        )
    
    return key