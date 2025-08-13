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
from typing import Any, Dict, Iterable, List, Optional

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


def call_and_save(method: Any, params: Dict[str, Any], path: Path, description: str) -> Any:
    """Call ``method`` with ``params`` and persist the response."""
    try:  # pragma: no cover - network/HTTP errors
        response = method(**params)
    except Exception as exc:  # pragma: no cover - network/HTTP errors
        response = {"error": str(exc)}
    save_json(path, description, params, response)
    return response


def _extract_original_uid(order: Dict[str, Any]) -> Optional[str]:
    """Best-effort extraction of a counterparty UID from an order object."""
    potential_keys: Iterable[str] = (
        "originalUid",
        "counterpartyUid",
        "otherUid",
        "uid",
        "userId",
        "buyerUid",
        "sellerUid",
    )
    for key in potential_keys:
        value = order.get(key)
        if value:
            return str(value)
    return None


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

    # Basic account information
    call_and_save(
        client.get_current_balance,
        {"accountType": "FUND"},
        base / "current_balance" / "balance.json",
        "Current balance for FUND account",
    )
    call_and_save(
        client.get_account_information,
        {},
        base / "account_information" / "account_information.json",
        "Account information",
    )

    for side_name, side_value in SIDES.items():
        for currency in CURRENCIES:
            # Competitor advertisements
            online_params = {
                "tokenId": TOKEN_ID,
                "currencyId": currency,  # camelCase
                "side": side_value,      # scalar int (0/1)
                "page": 1,
                "size": 10,
            }
            online_resp = call_and_save(
                client.get_online_ads,
                online_params,
                base / "competitor_ads" / side_name / currency / "response.json",
                f"Online advertisements for {side_name} {TOKEN_ID} in {currency}",
            )

            # My advertisements
            my_ads_params = {
                "tokenId": TOKEN_ID,
                "currencyId": currency,  # camelCase (was currency_id)
                "side": side_value,
                "page": 1,
                "size": 10,
            }
            my_ads_resp = call_and_save(
                client.get_ads_list,
                my_ads_params,
                base / "my_ads" / side_name / currency / "response.json",
                f"My advertisements for {side_name} {TOKEN_ID} in {currency}",
            )

            # Orders and grouped orders by status
            order_params = {
                # "tokenId": TOKEN_ID,   # not required for get_orders; may cause 10001 on some variants
                "side": side_value,      # scalar, not list
                "page": 1,
                "size": 50,
            }
            orders_resp = call_and_save(
                client.get_orders,
                order_params,
                base / "orders" / side_name / currency / "all_orders.json",
                f"All orders for {side_name} {TOKEN_ID}",
            )
            call_and_save(
                client.get_pending_orders,
                order_params,
                base / "pending_orders" / side_name / currency / "all_pending_orders.json",
                f"Pending orders for {side_name} {TOKEN_ID}",
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
                            base / "orders" / side_name / currency / f"status_{status}.json",
                            f"Example order with status {status} for {side_name} {TOKEN_ID} in {currency}",
                            order_params,
                            order,
                        )
                    if not first_order_for_currency:
                        first_order_for_currency = order

                # Order details & extras for the first order found for this currency
                if first_order_for_currency:
                    order_id = first_order_for_currency.get("orderId") or first_order_for_currency.get("id")
                    if order_id:
                        call_and_save(
                            client.get_order_details,
                            {"orderId": order_id},
                            base / "order_details" / side_name / currency / f"{order_id}.json",
                            f"Order details for {order_id}",
                        )
                        original_uid = _extract_original_uid(first_order_for_currency)
                        if original_uid:
                            call_and_save(
                                client.get_counterparty_info,
                                {"originalUid": original_uid, "orderId": order_id},
                                base / "counterparty_info" / side_name / currency / f"{order_id}.json",
                                f"Counterparty info for order {order_id}",
                            )
                        call_and_save(
                            client.get_chat_messages,
                            {"orderId": order_id, "startMessageId": 0, "size": 100},
                            base / "chat_messages" / side_name / currency / f"{order_id}.json",
                            f"Chat messages for order {order_id}",
                        )
                else:
                    # Placeholders for missing orders
                    placeholder_id = "0"
                    call_and_save(
                        client.get_order_details,
                        {"orderId": placeholder_id},
                        base / "order_details" / side_name / currency / "none.json",
                        "Order details placeholder",
                    )
                    call_and_save(
                        client.get_counterparty_info,
                        {"originalUid": "0", "orderId": placeholder_id},
                        base / "counterparty_info" / side_name / currency / "none.json",
                        "Counterparty info placeholder",
                    )
                    call_and_save(
                        client.get_chat_messages,
                        {"orderId": placeholder_id, "startMessageId": 0, "size": 100},
                        base / "chat_messages" / side_name / currency / "none.json",
                        "Chat messages placeholder",
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
                        call_and_save(
                            client.get_ad_details,
                            {"itemId": ad_id},
                            base / "ad_details" / side_name / currency / f"{ad_id}.json",
                            f"Ad details for {ad_id}",
                        )

    # Payment methods
    call_and_save(
        client.get_user_payment_types,
        {},
        base / "payment_methods" / "payment_methods.json",
        "User payment methods",
    )


if __name__ == "__main__":
    collect()
