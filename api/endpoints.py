"""WooCommerce Store API endpoint paths (public, no auth required for reads).

total.coffee runs WooCommerce with the block-based cart/checkout, which is
powered by the public `wc/store/v1` REST namespace. These paths are
relative (no leading slash) since they're joined against
CONFIG.api_base_url (".../wp-json/", with a trailing slash) via
Playwright's APIRequestContext base_url - a leading slash would resolve
as root-relative and silently drop the "/wp-json" prefix.
"""

PRODUCTS = "wc/store/v1/products"
PRODUCT_BY_ID = "wc/store/v1/products/{id}"
CATEGORIES = "wc/store/v1/products/categories"
CART = "wc/store/v1/cart"
CART_ADD_ITEM = "wc/store/v1/cart/add-item"
CART_UPDATE_ITEM = "wc/store/v1/cart/update-item"
CART_REMOVE_ITEM = "wc/store/v1/cart/remove-item"

# Core WordPress REST API - used to prove authenticated-only endpoints
# correctly reject anonymous access.
WP_ROOT = ""
WP_USERS = "wp/v2/users"
WP_POSTS = "wp/v2/posts"
