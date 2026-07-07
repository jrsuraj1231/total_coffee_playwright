"""Request payload builders for the WooCommerce Store API."""
from typing import Any


def add_item_payload(product_id: int, quantity: int = 1, variation: list[dict] | None = None) -> dict[str, Any]:
    payload: dict[str, Any] = {"id": product_id, "quantity": quantity}
    if variation:
        payload["variation"] = variation
    return payload


def update_item_payload(cart_item_key: str, quantity: int) -> dict[str, Any]:
    return {"key": cart_item_key, "quantity": quantity}


def remove_item_payload(cart_item_key: str) -> dict[str, Any]:
    return {"key": cart_item_key}
