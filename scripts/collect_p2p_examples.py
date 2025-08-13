"""Collect sample responses from Bybit P2P API and save them as JSON files.

This utility queries several endpoints of the :mod:`bybit_p2p` library and
stores the raw responses together with the request parameters and a short
description. Results are written under the ``examples`` directory grouped by
request type, trade side and fiat currency.

Required environment variables:
    - ``BYBIT_API_KEY``
    - ``BYBIT_API_SECRET``

Optional environment variables:
    - ``BYBIT_TESTNET`` (default: ``false``)
    - ``BYBIT_RECV_WINDOW`` (default: ``20000``)

Usage::

    python scripts/collect_p2p_examples.py
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List

from bybit_p2p import P2P

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))
from src.app.config import Settings

# Disable proxy settings that may block requests in some environments
os.environ["NO_PROXY"] = "*"
os.environ["HTTP_PROXY"] = ""
os.environ["HTTPS_PROXY"] = ""
os.environ["ALL_PROXY"] = ""


SIDES = {"BUY": 0, "SELL": 1}
CURRENCIES = ["UAH", "PLN"]
TOKEN_ID = "USDT"


def save_json(path: Path, description: str, request: Dict[str, Any], response: Any) -> None:
    """Persist data to ``path`` in a readable JSON format."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        json.dump(
            {
                "description": description,
                "request": request,
                "response": response,
            },
            fh,
            ensure_ascii=False,
            indent=2,
        )


def collect() -> None:
    """Execute all API requests and store responses."""
    settings = Settings.from_env()
    client = P2P(
        testnet=settings.testnet,
        api_key=settings.api_key,
        api_secret=settings.api_secret,
        recv_window=settings.recv_window,
    )

    base = Path("examples")

    for side_name, side_value in SIDES.items():
        for currency in CURRENCIES:
            # Competitor advertisements
            online_params = {
                "tokenId": TOKEN_ID,
                "currencyId": currency,
                "side": side_value,
                "page": 1,
                "size": 10,
            }
            try:
                online_resp = client.get_online_ads(**online_params)
            except Exception as exc:  # pragma: no cover - network errors
                online_resp = {"error": str(exc)}
            save_json(
                base / "competitor_ads" / side_name / currency / "response.json",
                f"Online advertisements for {side_name} {TOKEN_ID} in {currency}",
                online_params,
                online_resp,
            )

            # My advertisements
            my_ads_params = {
                "tokenId": TOKEN_ID,
                "currency_id": currency,
                "side": side_value,
                "page": 1,
                "size": 10,
            }
            try:
                my_ads_resp = client.get_ads_list(**my_ads_params)
            except Exception as exc:  # pragma: no cover
                my_ads_resp = {"error": str(exc)}
            save_json(
                base / "my_ads" / side_name / currency / "response.json",
                f"My advertisements for {side_name} {TOKEN_ID} in {currency}",
                my_ads_params,
                my_ads_resp,
            )

            # Orders and grouped orders by status
            order_params = {
                "tokenId": TOKEN_ID,
                "side": [side_value],
                "page": 1,
                "size": 50,
            }
            try:
                orders_resp = client.get_orders(**order_params)
            except Exception as exc:  # pragma: no cover
                orders_resp = {"error": str(exc)}
            save_json(
                base / "orders" / side_name / currency / "all_orders.json",
                f"All orders for {side_name} {TOKEN_ID}",
                order_params,
                orders_resp,
            )

            if "error" not in orders_resp:
                orders: List[Dict[str, Any]] = (
                    orders_resp.get("result", {}).get("list")
                    or orders_resp.get("result", {}).get("items")
                    or []
                )
                seen_status: Dict[str, bool] = {}
                first_order_for_currency = None
                for order in orders:
                    fiat = order.get("currencyId") or order.get("currency")
                    if fiat != currency:
                        continue
                    status = str(order.get("status"))
                    if status not in seen_status:
                        seen_status[status] = True
                        save_json(
                            base
                            / "orders"
                            / side_name
                            / currency
                            / f"status_{status}.json",
                            f"Example order with status {status} for {side_name} {TOKEN_ID} in {currency}",
                            order_params,
                            order,
                        )
                    if not first_order_for_currency:
                        first_order_for_currency = order

                # Order details for the first order found for this currency
                if first_order_for_currency:
                    order_id = first_order_for_currency.get("orderId") or first_order_for_currency.get("id")
                    if order_id:
                        try:
                            details_resp = client.get_order_details(orderId=order_id)
                        except Exception as exc:  # pragma: no cover
                            details_resp = {"error": str(exc)}
                        save_json(
                            base / "order_details" / side_name / currency / f"{order_id}.json",
                            f"Order details for {order_id}",
                            {"orderId": order_id},
                            details_resp,
                        )

            # Ad details for the first advertisement
            if "error" not in my_ads_resp:
                my_ads: List[Dict[str, Any]] = (
                    my_ads_resp.get("result", {}).get("list")
                    or my_ads_resp.get("result", {}).get("items")
                    or []
                )
                if my_ads:
                    ad_id = my_ads[0].get("itemId") or my_ads[0].get("id")
                    if ad_id:
                        try:
                            ad_details_resp = client.get_ad_details(itemId=ad_id)
                        except Exception as exc:  # pragma: no cover
                            ad_details_resp = {"error": str(exc)}
                        save_json(
                            base / "ad_details" / side_name / currency / f"{ad_id}.json",
                            f"Ad details for {ad_id}",
                            {"itemId": ad_id},
                            ad_details_resp,
                        )

    # Payment methods
    try:
        payment_resp = client.get_user_payment_types()
    except Exception as exc:  # pragma: no cover
        payment_resp = {"error": str(exc)}
    save_json(
        base / "payment_methods" / "payment_methods.json",
        "User payment methods",
        {},
        payment_resp,
    )


if __name__ == "__main__":
    collect()

