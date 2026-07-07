"""Locators for the logged-in My Account dashboard (order history, addresses,
downloads, account details, logout)."""


class AccountLocators:
    NAV = ".woocommerce-MyAccount-navigation"
    NAV_ORDERS = ".woocommerce-MyAccount-navigation-link--orders a"
    NAV_DOWNLOADS = ".woocommerce-MyAccount-navigation-link--downloads a"
    NAV_ADDRESSES = ".woocommerce-MyAccount-navigation-link--edit-address a"
    NAV_ACCOUNT_DETAILS = ".woocommerce-MyAccount-navigation-link--edit-account a"
    NAV_LOGOUT = ".woocommerce-MyAccount-navigation-link--customer-logout a"
    DASHBOARD_GREETING = ".woocommerce-MyAccount-content p"
    ORDERS_TABLE = ".woocommerce-orders-table"
    NO_ORDERS_MESSAGE = ".woocommerce-message, .woocommerce-info"
