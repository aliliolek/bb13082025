"""Bybit P2P client helpers."""

from bybit_p2p import P2P


def get_api(config: dict) -> P2P:
    """Instantiate a Bybit P2P API client from config."""
    return P2P(api_key=config["api_key"], api_secret=config["api_secret"])
