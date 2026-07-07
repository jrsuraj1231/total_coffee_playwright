"""Page Object for header search + the resulting product-listing page.

WooCommerce search results render on the shop archive template using
?s=<term>&post_type=product, and reuse the same product-grid markup as
category pages.
"""
from urllib.parse import quote_plus

from playwright.sync_api import Page

from components.header import Header
from pages.base_page import BasePage


class SearchPage(BasePage):
    RESULTS_HEADING = "h1.woocommerce-products-header__title, h1.page-title"
    PRODUCT_LIST_ITEM = "ul.products li.product"
    PRODUCT_LINK = "li.product a.woocommerce-LoopProduct-link"
    NO_RESULTS_MESSAGE = ".woocommerce-info, p.no-products-found"

    def __init__(self, page: Page):
        super().__init__(page)
        self.header = Header(page)
        self.results_heading = page.locator(self.RESULTS_HEADING)
        self.product_items = page.locator(self.PRODUCT_LIST_ITEM)
        self.product_links = page.locator(self.PRODUCT_LINK)
        self.no_results_message = page.locator(self.NO_RESULTS_MESSAGE)

    def search_via_url(self, term: str) -> "SearchPage":
        self.goto(f"/?s={quote_plus(term)}&post_type=product")
        return self

    def search_via_header(self, term: str) -> "SearchPage":
        self.header.search_for(term)
        return self

    def result_count(self) -> int:
        return self.product_items.count()

    def has_results(self) -> bool:
        return self.result_count() > 0

    def is_no_results_message_visible(self) -> bool:
        return self.is_visible(self.no_results_message)

    def result_titles(self) -> list[str]:
        return self.product_items.locator("h2, h3").all_inner_texts()

    def open_result(self, index: int = 0) -> None:
        self.product_links.nth(index).click()
