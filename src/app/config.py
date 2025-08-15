"""Application configuration utilities."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any, Dict

import yaml
from dotenv import load_dotenv


@dataclass
class Settings:
    """Holds configuration loaded from config.yaml and environment variables."""

    api_key: str
    api_secret: str
    testnet: bool = False
    recv_window: int = 20000
    poll_interval_price: int = 60
    poll_interval_balance: int = 300
    min_payment_method_matches: int = 1
    payment_methods: Dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_file(cls, path: str = "config.yaml") -> "Settings":
        """Create settings from a YAML file and environment variables."""
        load_dotenv()
        with open(path, "r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh) or {}

        bybit_cfg = data.get("bybit", {})
        polling_cfg = data.get("polling", {})
        payments_cfg = data.get("payments", {})

        api_key = os.getenv("BYBIT_API_KEY")
        api_secret = os.getenv("BYBIT_API_SECRET")
        if not api_key or not api_secret:
            raise RuntimeError(
                "BYBIT_API_KEY and BYBIT_API_SECRET environment variables are required"
            )

        def _positive_int(value: Any, default: int) -> int:
            try:
                ivalue = int(value)
                return ivalue if ivalue > 0 else default
            except (TypeError, ValueError):
                return default

        return cls(
            api_key=api_key,
            api_secret=api_secret,
            testnet=bool(bybit_cfg.get("testnet", False)),
            recv_window=_positive_int(bybit_cfg.get("recv_window"), 20000),
            poll_interval_price=_positive_int(polling_cfg.get("price"), 60),
            poll_interval_balance=_positive_int(polling_cfg.get("balance"), 300),
            min_payment_method_matches=_positive_int(payments_cfg.get("min_match_count"), 1),
            payment_methods=payments_cfg.get("mappings", {}) or {},
        )
