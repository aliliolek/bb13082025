"""Configuration utilities for the Bybit P2P client."""

from os import getenv

try:  # Prefer local .env when available
    from dotenv import load_dotenv

    load_dotenv()
except Exception:  # pragma: no cover - dotenv is optional
    pass


def load_config() -> dict:
    """Load required API settings from environment variables."""
    api_key = getenv("BYBIT_API_KEY")
    api_secret = getenv("BYBIT_API_SECRET")
    if not api_key or not api_secret:
        raise RuntimeError("BYBIT_API_KEY and BYBIT_API_SECRET must be set")
    return {"api_key": api_key, "api_secret": api_secret}
