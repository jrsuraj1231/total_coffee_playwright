"""Site header component: nav menu, search box, login link, basket trigger."""
from playwright.sync_api import Page


class Header:
    SEARCH_INPUT = "#nm-header-search-input"

    def __init__(self, page: Page):
        self.page = page
        self.login_link = page.locator("#nm-menu-account-btn")
        self.basket_link = page.locator("#nm-menu-cart-btn")
        self.search_trigger = page.locator("#nm-menu-search-btn")
        self.search_input = page.locator(self.SEARCH_INPUT)
        self.nav_menu = page.locator("#nm-main-menu-ul")

    def search_for(self, term: str) -> None:
        self.search_trigger.click()
        self.search_input.wait_for(state="visible")
        self.search_input.fill(term)
        self.search_input.press("Enter")

    def open_login(self) -> None:
        self.login_link.click()

    def open_basket_drawer(self) -> None:
        self.basket_link.click()

    def go_to_category(self, category_name: str) -> None:
        self.nav_menu.get_by_role("link", name=category_name, exact=True).first.click()
