"""Entry point for the sample application."""

from pprint import pprint

from pathlib import Path

from .api_client import BybitP2PClient
from .config import Settings


def main() -> None:
    """Run the application."""
    settings = Settings.from_file(Path(__file__).resolve().parents[1] / "config.yaml")
    client = BybitP2PClient(
        settings.api_key,
        settings.api_secret,
        settings.testnet,
        recv_window=settings.recv_window,
    )
    # order = client.get_latest_order()
    # pprint(order)

    for s in ("0", "1"):  # None = both, 0 = BUY, 1 = SELL
        resp = client._client.get_orders(
            page="1",
            size="10",
            # tokenId="USDT",
            # status="50",  # Completed
            # side=s,  # None, 0, or 1
            # beginTime=beginTime,
            # endTime=endTime,
        )

        pprint(resp)


if __name__ == "__main__":
    main()
