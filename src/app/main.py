"""Entry point for the sample application."""

import json
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
    # order = client.get_latest_order()
    # pprint(order)

    for s in ("0", "1"):  # None = both, 0 = BUY, 1 = SELL
      beginTime = "1751328000000"  # 2025-07-01 00:00:00 UTC
      endTime   = "1754006399999"  # 2025-07-31 23:59:59 UTC

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
