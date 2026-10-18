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