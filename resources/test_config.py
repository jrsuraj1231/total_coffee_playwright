"""Convenience re-export of the active config plus pytest marker names.

Kept separate from config/config.py so tests can do:
    from resources.test_config import CONFIG, Markers
without reaching into the config package directly.
"""
from config.config import CONFIG


class Markers:
    SMOKE = "smoke"
    REGRESSION = "regression"
    API = "api"
    CART = "cart"
    SEARCH = "search"
    PRODUCT = "product"
    ACCOUNT = "account"
    CHECKOUT = "checkout"


__all__ = ["CONFIG", "Markers"]
