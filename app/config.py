"""Configuration utilities for the Bybit P2P client."""

from os import getenv

try:  # Prefer local .env when available
    from dotenv import load_dotenv

    load_dotenv()
except Exception:  # pragma: no cover - dotenv is optional
    pass


def load_config() -> dict:
    """Load API credentials and flags from environment variables."""
    api_key = getenv("BYBIT_API_KEY")
    api_secret = getenv("BYBIT_API_SECRET")
    testnet = getenv("BYBIT_TESTNET", "false").lower() in {"1", "true", "yes"}
    recv_window = int(getenv("BYBIT_RECV_WINDOW", "20000"))
    if not api_key or not api_secret:
        raise RuntimeError("BYBIT_API_KEY and BYBIT_API_SECRET must be set")
    return {
        "api_key": api_key,
        "api_secret": api_secret,
        "testnet": testnet,
        "recv_window": recv_window,
    }

