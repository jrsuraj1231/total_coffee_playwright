"""Locators for the mini-cart ('Basket') drawer and the /cart/ page.

Confirmed against the live total.coffee DOM: despite the theme
stylesheet referencing WooCommerce Blocks class names, /cart/ actually
renders the classic WooCommerce shortcode cart (form.woocommerce-cart-form,
table.cart, tr.cart_item), and the store's translation strings rename
"cart" to "basket" throughout ("Update cart" -> "Update basket", etc.).
"""


class MiniCartLocators:
    PANEL = ".cart-panel, #nm-cart-panel"
    PANEL_TITLE = "text=Basket"
    PANEL_CLOSE_BUTTON = ".cart-panel .cart-panel-close, .cart-panel button[aria-label='Close']"
    CONTINUE_SHOPPING_LINK = "a:has-text('Continue shopping')"
    CART_COUNT_BADGE = ".nm-menu-cart-count, [class*='cart-count']"


class CartPageLocators:
    FORM = "form.woocommerce-cart-form"
    EMPTY_CART_MESSAGE = ".wc-empty-cart-message"
    CART_ITEM_ROW = "tr.woocommerce-cart-form__cart-item"
    ITEM_PRODUCT_LINK = "td.nm-product-details a"
    ITEM_QUANTITY_INPUT = "input.qty"
    ITEM_REMOVE_LINK = "a.remove_from_cart_button"
    ITEM_SUBTOTAL = ".product-subtotal .woocommerce-Price-amount"
    UPDATE_CART_BUTTON = "button[name='update_cart']"
    CONTINUE_SHOPPING_BUTTON = "#nm-cart-continue-button"
    CART_SUBTOTAL_ROW = "tr.cart-subtotal .woocommerce-Price-amount"
    ORDER_TOTAL_ROW = "tr.order-total .woocommerce-Price-amount"
    PROCEED_TO_CHECKOUT_BUTTON = "a.checkout-button"
