"""Framework-wide constants: URL paths, WooCommerce Store API routes, messages."""

# --- Site paths (relative to base_url) ---------------------------------
PATH_HOME = "/"
PATH_MY_ACCOUNT = "/my-account/"
PATH_LOST_PASSWORD = "/my-account/lost-password/"
PATH_CART = "/cart/"
PATH_CHECKOUT = "/checkout/"
PATH_SHOP = "/shop/"
PATH_SEARCH = "/"  # search is a query string on the home/shop route: ?s=<term>

# --- WooCommerce Store API routes (relative to api_base_url, no leading
# slash - api_base_url ends with a trailing slash so paths join correctly) ---
API_STORE_PRODUCTS = "wc/store/v1/products"
API_STORE_PRODUCT_BY_ID = "wc/store/v1/products/{id}"
API_STORE_CATEGORIES = "wc/store/v1/products/categories"
API_STORE_CART = "wc/store/v1/cart"
API_STORE_CART_ADD_ITEM = "wc/store/v1/cart/add-item"
API_STORE_CART_UPDATE_ITEM = "wc/store/v1/cart/update-item"
API_STORE_CART_REMOVE_ITEM = "wc/store/v1/cart/remove-item"
API_WP_ROOT = ""
API_WP_USERS = "wp/v2/users"
API_WP_POSTS = "wp/v2/posts"

# --- Expected UI text / messages ----------------------------------------
MSG_EMPTY_CART = "Your cart is currently empty"
MSG_INVALID_LOGIN = "unknown email address"
MSG_LOGIN_ERROR_GENERIC = "error"

# --- Misc -----------------------------------------------------------------
DEFAULT_CURRENCY_SYMBOL = "₹"  # INR rupee symbol used across the store
SCREENSHOT_DIR = "screenshots/failures"
LOG_DIR = "logs"
