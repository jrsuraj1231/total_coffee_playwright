"""Locators for the product detail page (PDP) and product-listing/search
result grids - confirmed against the live total.coffee DOM (WooCommerce +
Savoy theme)."""


class ProductLocators:
    TITLE = "h1.product_title"
    PRICE = "p.price, span.price"
    QUANTITY_INPUT = "input[name='quantity']"
    ADD_TO_CART_BUTTON = "button.single_add_to_cart_button"
    READ_MORE_BUTTON = "a.product_type_variable, a.button.product_type_simple"
    BREADCRUMB = ".woocommerce-breadcrumb"
    STOCK_STATUS = "p.stock"
    SHORT_DESCRIPTION = ".woocommerce-product-details__short-description"
    ADDED_TO_CART_MESSAGE = ".woocommerce-message"


class ProductGridLocators:
    """Used on category / shop / search-result listing pages."""

    PRODUCT_LIST_ITEM = "ul.products li.product"
    PRODUCT_LINK = "li.product a.woocommerce-LoopProduct-link"
    PRODUCT_TITLE = "li.product h2, li.product h3"
    PRODUCT_PRICE = "li.product span.price"
    ADD_TO_BASKET_LINK = "li.product a.add_to_cart_button"
    NO_RESULTS_MESSAGE = ".woocommerce-info, p.no-products-found"
