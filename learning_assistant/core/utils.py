import os
import google.generativeai as genai
from .exceptions import ConfigurationError

def get_gemini_model(model_name='gemini-2.5-flash-lite'):
    """
    Configures Gemini and returns a GenerativeModel instance.
    Raises ConfigurationError if GEMINI_API_KEY is not set.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ConfigurationError("GEMINI_API_KEY not configured in .env file")
    
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(model_name)
