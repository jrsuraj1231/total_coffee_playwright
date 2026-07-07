"""Page Object for the logged-in My Account dashboard."""
from playwright.sync_api import Page

from pages.base_page import BasePage


class DashboardPage(BasePage):
    PATH = "/my-account/"

    NAV = ".woocommerce-MyAccount-navigation"
    NAV_ORDERS = ".woocommerce-MyAccount-navigation-link--orders a"
    NAV_DOWNLOADS = ".woocommerce-MyAccount-navigation-link--downloads a"
    NAV_ADDRESSES = ".woocommerce-MyAccount-navigation-link--edit-address a"
    NAV_ACCOUNT_DETAILS = ".woocommerce-MyAccount-navigation-link--edit-account a"
    NAV_LOGOUT = ".woocommerce-MyAccount-navigation-link--customer-logout a"
    DASHBOARD_GREETING = ".woocommerce-MyAccount-content p"
    ORDERS_TABLE = ".woocommerce-orders-table"
    NO_ORDERS_MESSAGE = ".woocommerce-message, .woocommerce-info"

    def __init__(self, page: Page):
        super().__init__(page)
        self.nav = page.locator(self.NAV)
        self.orders_link = page.locator(self.NAV_ORDERS)
        self.downloads_link = page.locator(self.NAV_DOWNLOADS)
        self.addresses_link = page.locator(self.NAV_ADDRESSES)
        self.account_details_link = page.locator(self.NAV_ACCOUNT_DETAILS)
        self.logout_link = page.locator(self.NAV_LOGOUT)
        self.greeting = page.locator(self.DASHBOARD_GREETING)
        self.orders_table = page.locator(self.ORDERS_TABLE)
        self.no_orders_message = page.locator(self.NO_ORDERS_MESSAGE)

    def open(self) -> "DashboardPage":
        self.goto(self.PATH)
        return self

    def is_nav_visible(self) -> bool:
        return self.is_visible(self.nav)

    def go_to_orders(self) -> None:
        self.click(self.orders_link)

    def go_to_downloads(self) -> None:
        self.click(self.downloads_link)

    def go_to_addresses(self) -> None:
        self.click(self.addresses_link)

    def go_to_account_details(self) -> None:
        self.click(self.account_details_link)

    def has_orders(self) -> bool:
        return self.is_visible(self.orders_table)
