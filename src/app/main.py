"""Entry point for the sample application."""

from pprint import pprint

from .api_client import BybitP2PClient
from .config import Settings


def main() -> None:
    """Run the application."""
    settings = Settings.from_env()
    client = BybitP2PClient(
        settings.api_key,
        settings.api_secret,
        settings.testnet,
        recv_window=settings.recv_window,
    )
    order = client.get_latest_order()
    pprint(order)


if __name__ == "__main__":
    main()
