"""Wrapper around the official Bybit P2P client."""

from __future__ import annotations

from ctypes import Union
from typing import Any, Dict, List, Optional

from bybit_p2p import P2P


class BybitP2PClient:
    """Minimal helper for interacting with Bybit's P2P API.

    This class delegates all work to the `bybit_p2p` library while exposing a
    small, easy-to-use surface for the application.
    """

    def __init__(
        self, api_key: str, api_secret: str, testnet: bool, *, recv_window: int = 20000
    ) -> None:
        self._client = P2P(
            testnet=testnet,
            api_key=api_key,
            api_secret=api_secret,
            recv_window=recv_window,
        )

    def get_latest_order(self) -> Optional[Dict[str, Any]]:
        """Fetch the most recent order from the user's history."""
        response = self._client.get_orders(page=1, size=1)
        result = response.get("result") or {}
        orders = result.get("list") or result.get("items") or []
        return orders[0] if orders else None