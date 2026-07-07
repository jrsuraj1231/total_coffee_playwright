"""Locators for /checkout/ - confirmed against the live total.coffee DOM as
the classic WooCommerce shortcode checkout (form[name='checkout'],
billing_* field ids), not WooCommerce Blocks.

Safety note: automated tests must never actually complete this form and
submit #place_order, since it charges/creates a real order on a live
production store. Only field-level and validation-message assertions are
performed - see pages/checkout_page.py.
"""


class CheckoutLocators:
    FORM = "form[name='checkout']"
    EMPTY_CART_NOTICE = ".wc-empty-cart-message, .cart-empty"

    BILLING_FIRST_NAME = "#billing_first_name"
    BILLING_LAST_NAME = "#billing_last_name"
    BILLING_ADDRESS_1 = "#billing_address_1"
    BILLING_CITY = "#billing_city"
    BILLING_STATE = "#billing_state"
    BILLING_POSTCODE = "#billing_postcode"
    BILLING_PHONE = "#billing_phone"
    BILLING_EMAIL = "#billing_email"

    ORDER_REVIEW = "#order_review"
    ORDER_REVIEW_HEADING = "#order_review_heading"
    PLACE_ORDER_BUTTON = "#place_order"
    TERMS_CHECKBOX = "#terms"

    VALIDATION_ERROR_NOTICE = ".woocommerce-error, .woocommerce-NoticeGroup"
    INVALID_FIELD = ".woocommerce-invalid"
