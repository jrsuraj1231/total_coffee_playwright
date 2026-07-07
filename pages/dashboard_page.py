"""Page Object for the logged-in My Account dashboard."""
from playwright.sync_api import Page

from locators.account_locator import AccountLocators
from pages.base_page import BasePage
from resources.constants import PATH_MY_ACCOUNT


class DashboardPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.nav = page.locator(AccountLocators.NAV)
        self.orders_link = page.locator(AccountLocators.NAV_ORDERS)
        self.downloads_link = page.locator(AccountLocators.NAV_DOWNLOADS)
        self.addresses_link = page.locator(AccountLocators.NAV_ADDRESSES)
        self.account_details_link = page.locator(AccountLocators.NAV_ACCOUNT_DETAILS)
        self.logout_link = page.locator(AccountLocators.NAV_LOGOUT)
        self.greeting = page.locator(AccountLocators.DASHBOARD_GREETING)
        self.orders_table = page.locator(AccountLocators.ORDERS_TABLE)
        self.no_orders_message = page.locator(AccountLocators.NO_ORDERS_MESSAGE)

    def open(self) -> "DashboardPage":
        self.goto(PATH_MY_ACCOUNT)
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
