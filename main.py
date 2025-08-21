"""Entrypoint for the Bybit P2P project."""

from app.client.bybit import get_api
from app.config import load_config


def main() -> None:
    config = load_config()
    client = get_api(config)
    print(client.get_pending_orders())


if __name__ == "__main__":
    main()
