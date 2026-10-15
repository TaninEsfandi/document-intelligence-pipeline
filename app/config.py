import os
from pathlib import Path
from dotenv import load_dotenv

# Explicit path so .env is found regardless of cwd (e.g. MCP server launched from "/").
# Existing environment variables (e.g. from docker-compose) take precedence over .env.
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
FDA_API_URL = os.getenv("FDA_API_URL", "https://api.fda.gov/device/event.json")
