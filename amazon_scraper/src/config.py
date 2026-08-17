import os
from pathlib import Path
from dotenv import load_dotenv

# Absolute path to the project root .env
env_path = Path(__file__).resolve().parent.parent / ".env"

print(f"Looking for .env at: {env_path}")
print(f"File exists: {env_path.exists()}")

loaded = load_dotenv(dotenv_path=env_path)

print(f"load_dotenv() returned: {loaded}")

ASIN_API_KEY = os.getenv("ASIN_API_KEY")

print(f"API Key: {ASIN_API_KEY}")

# ASIN Data API configuration
API_URL = "https://api.asindataapi.com/request"
AMAZON_DOMAIN = "amazon.com"

if not ASIN_API_KEY:
    raise ValueError("ASIN_API_KEY not found in .env")