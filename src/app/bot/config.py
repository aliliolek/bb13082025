"""Configuration for the Telegram bot."""

from __future__ import annotations

import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


def _env_int(name: str) -> int:
    value = os.getenv(name)
    if value is None:
        raise RuntimeError(f"{name} environment variable is required")
    try:
        return int(value)
    except ValueError as exc:
        raise RuntimeError(f"{name} must be an integer") from exc


@dataclass
class BotSettings:
    """Settings loaded from environment variables."""

    token: str
    admin_id: int

    @classmethod
    def from_env(cls) -> "BotSettings":
        token = os.getenv("TG_BOT_TOKEN")
        if not token:
            raise RuntimeError("TG_BOT_TOKEN environment variable is required")
        admin_id = _env_int("TG_ADMIN_ID")
        return cls(token=token, admin_id=admin_id)
