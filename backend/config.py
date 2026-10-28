"""
Food Verse AI - Backend Configuration
======================================
Loads environment variables and sets up application configuration.
"""

import os

# Project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_env_file():
    """Simple parser for .env file."""
    env_path = os.path.join(BASE_DIR, ".env")
    if os.path.exists(env_path):
        try:
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "=" in line:
                        key, val = line.split("=", 1)
                        os.environ[key.strip()] = val.strip().strip('"').strip("'")
        except Exception as e:
            print(f"[Warning] Failed to read .env: {e}")

load_env_file()

def get_gemini_api_key() -> str:
    """Retrieves GEMINI_API_KEY from environment, ignoring placeholder values."""
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not key:
        return ""
    lower = key.lower()
    if lower in ("your_gemini_api_key_here", "your_api_key_here", "none", "null", "placeholder"):
        return ""
    if lower.startswith("your_") or lower.startswith("<") or len(key) < 15:
        return ""
    return key

def is_ai_enabled() -> bool:
    """True only if a valid, non-placeholder Gemini API key is configured."""
    return bool(get_gemini_api_key())
