import os
from typing import Optional
from dotenv import load_dotenv, find_dotenv


# Load .env file into process environment (if present). Use find_dotenv to
# locate the file reliably even if the current working directory changes.
dotenv_path = find_dotenv()
if dotenv_path:
    load_dotenv(dotenv_path)


class Settings:
    """Lightweight settings loader using environment variables.

    Loads environment from a .env file via python-dotenv so values defined
    in `.env` are available to the running process without manual export.
    """
    OPENROUTER_API_KEY: Optional[str] = os.getenv("OPENROUTER_API_KEY")
    OPENROUTER_URL: str = os.getenv("OPENROUTER_URL", "https://api.openrouter.ai/v1/chat/completions")
    OPENROUTER_MODEL: str = os.getenv("OPENROUTER_MODEL", "gpt-4o-mini")

    TAVILY_API_KEY: Optional[str] = os.getenv("TAVILY_API_KEY")
    TAVILY_API_URL: str = os.getenv("TAVILY_API_URL", "https://api.tavily.com/search")

