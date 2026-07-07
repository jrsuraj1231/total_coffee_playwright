"""API tests against the public WooCommerce Store API (wc/store/v1).

Cart mutations (add/remove) are safe and non-destructive: they only
change the anonymous session's cart, never place a real order. No test
in this file ever calls the checkout/order-placement endpoint.
"""
import json

import pytest

from api.endpoints import CART, CART_ADD_ITEM, CART_REMOVE_ITEM, CATEGORIES, PRODUCT_BY_ID, PRODUCTS
from api.payloads import add_item_payload, remove_item_payload

PRODUCT_IDS = [16330, 2528, 14374]  # aeropress-flow-control-filter-cap, cafflano-kompact, fellow-stagg-pro


@pytest.mark.api
def test_get_products_list_returns_200_and_valid_schema(api_client):
    response = api_client.get(PRODUCTS, params={"per_page": 10})

    assert response.status == 200
    products = json.loads(response.text())
    assert len(products) > 0

    required_keys = {"id", "name", "slug", "type", "prices", "permalink"}
    for product in products:
        assert required_keys.issubset(product.keys())


@pytest.mark.api
@pytest.mark.parametrize("product_id", PRODUCT_IDS)
def test_get_single_product_by_id(api_client, product_id):
    response = api_client.get(PRODUCT_BY_ID.format(id=product_id))

    assert response.status == 200
    product = json.loads(response.text())
    assert product["id"] == product_id
    assert product["prices"]["currency_code"] == "INR"
    assert int(product["prices"]["price"]) > 0


@pytest.mark.api
def test_get_product_categories_returns_200(api_client):
    response = api_client.get(CATEGORIES, params={"per_page": 5})

    assert response.status == 200
    categories = json.loads(response.text())
    assert len(categories) > 0
    for category in categories:
        assert {"id", "name", "slug", "permalink"}.issubset(category.keys())


@pytest.mark.api
def test_add_and_remove_cart_item_via_store_api(api_client):
    product_id = PRODUCT_IDS[0]

    # GET first to obtain the Nonce/Cart-Token pair the Store API requires
    # for any mutating call.
    api_client.get(CART)

    add_response = api_client.post(CART_ADD_ITEM, data=add_item_payload(product_id, quantity=1))
    assert add_response.status == 201
    cart_after_add = json.loads(add_response.text())
    assert any(item["id"] == product_id for item in cart_after_add["items"])

    item_key = next(item["key"] for item in cart_after_add["items"] if item["id"] == product_id)

    remove_response = api_client.post(CART_REMOVE_ITEM, data=remove_item_payload(item_key))
    assert remove_response.status == 200
    cart_after_remove = json.loads(remove_response.text())
    assert not any(item["id"] == product_id for item in cart_after_remove["items"])
