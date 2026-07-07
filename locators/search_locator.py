"""Locators for the header search box and search-results listing.

Not in the originally requested locators/ list but added since pages/search_page.py
needs its own selectors distinct from product_locator.py's generic grid.
"""


class SearchLocators:
    SEARCH_INPUT = "#nm-header-search-input"
    SEARCH_FORM = "form[action='https://total.coffee/'][method='get']"
    SEARCH_ICON_TRIGGER = ".nm-header-search-trigger, [class*='search-trigger']"
    RESULTS_HEADING = "h1.woocommerce-products-header__title, h1.page-title"
