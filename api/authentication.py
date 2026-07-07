"""Auth/session handling for the WooCommerce Store API.

The Store API has no login endpoint of its own - cart state is tied to an
anonymous session identified by a `Cart-Token` (JWT) and mutating calls
(POST/PUT/DELETE) must echo back the `Nonce` value the API handed out on
the most recent GET. Both are returned as response headers.

There is no public write-capable REST endpoint on total.coffee that
accepts a real username/password (no JWT-auth plugin is installed), so
this framework does not attempt real customer login over the API - only
over the UI (see pages/login_page.py). test_login_api.py instead verifies
that credential-protected endpoints (e.g. /wp/v2/users) correctly reject
anonymous requests.
"""
from playwright.sync_api import APIRequestContext, APIResponse


class StoreApiSession:
    """Tracks the rolling Nonce/Cart-Token pair required for Store API writes."""

    def __init__(self, request_context: APIRequestContext):
        self._request_context = request_context
        self.nonce: str | None = None
        self.cart_token: str | None = None

    def capture_from_response(self, response: APIResponse) -> None:
        nonce = response.headers.get("nonce")
        cart_token = response.headers.get("cart-token")
        if nonce:
            self.nonce = nonce
        if cart_token:
            self.cart_token = cart_token

    def auth_headers(self) -> dict[str, str]:
        headers = {}
        if self.nonce:
            headers["Nonce"] = self.nonce
        if self.cart_token:
            headers["Cart-Token"] = self.cart_token
        return headers
