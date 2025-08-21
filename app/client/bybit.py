"""Bybit P2P client helpers."""

from bybit_p2p import P2P



def get_api(*, api_key: str, api_secret: str, testnet: bool, recv_window: int) -> P2P:
    """Instantiate a Bybit P2P API client."""
    return P2P(
        testnet=testnet,
        api_key=api_key,
        api_secret=api_secret,
        recv_window=recv_window,
    )

