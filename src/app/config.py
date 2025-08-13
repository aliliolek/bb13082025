"""Application configuration utilities."""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


def _env_bool(name: str, default: bool = False) -> bool:
    return os.getenv(name, str(default)).lower() in {"1", "true", "yes"}


def _env_int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, str(default)))
    except ValueError:
        return default


@dataclass
class Settings:
    """Holds configuration loaded from environment variables."""

    api_key: str
    api_secret: str
    testnet: bool = False
    recv_window: int = 20000

    @classmethod
    def from_env(cls) -> "Settings":
        """Create settings from environment variables."""
        api_key = os.getenv("BYBIT_API_KEY")
        api_secret = os.getenv("BYBIT_API_SECRET")
        if not api_key or not api_secret:
            raise RuntimeError(
                "BYBIT_API_KEY and BYBIT_API_SECRET environment variables are required",
            )
        testnet = _env_bool("BYBIT_TESTNET")
        recv_window = _env_int("BYBIT_RECV_WINDOW", 20000)
        return cls(
            api_key=api_key,
            api_secret=api_secret,
            testnet=testnet,
            recv_window=recv_window,
        )
