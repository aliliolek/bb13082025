"""Entrypoint for the Bybit P2P project."""

from app.client.bybit import get_api
from app.config import load_config


def main() -> None:
    config = load_config()
    client = get_api(
        api_key=config["api_key"],
        api_secret=config["api_secret"],
        testnet=config["testnet"],
        recv_window=config["recv_window"],
    )
    print(client.get_pending_orders())


if __name__ == "__main__":
    main()
