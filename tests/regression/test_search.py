"""Regression tests for header search and category navigation."""
import pytest

from pages.search_page import SearchPage
from utilities.json_reader import read_json
from utilities.yaml_reader import read_yaml

SEARCH_DATA = read_json("search_terms.json")
NAV_DATA = read_yaml("config.yaml")


@pytest.mark.regression
@pytest.mark.search
@pytest.mark.parametrize("case", SEARCH_DATA["valid_terms"], ids=[c["term"] for c in SEARCH_DATA["valid_terms"]])
def test_search_with_valid_keyword_returns_results(page, case):
    search_page = SearchPage(page).search_via_url(case["term"])

    assert search_page.has_results() == case["expect_results"]


@pytest.mark.regression
@pytest.mark.search
@pytest.mark.parametrize(
    "case", SEARCH_DATA["invalid_terms"], ids=[c["term"] for c in SEARCH_DATA["invalid_terms"]]
)
def test_search_with_invalid_keyword_returns_no_results(page, case):
    search_page = SearchPage(page).search_via_url(case["term"])

    assert not search_page.has_results()
    assert search_page.is_no_results_message_visible()


@pytest.mark.regression
@pytest.mark.search
def test_search_with_empty_keyword_shows_shop_listing(page):
    search_page = SearchPage(page).search_via_url("")

    # An empty search term falls back to the full product listing rather
    # than erroring, so results should still be present.
    assert search_page.has_results()


@pytest.mark.regression
@pytest.mark.search
def test_search_result_navigates_to_correct_product_page(page):
    search_page = SearchPage(page).search_via_url("AEROPRESS")
    assert search_page.has_results()

    search_page.open_result(0)

    assert "/shop/" in page.url


@pytest.mark.regression
@pytest.mark.search
def test_search_is_case_insensitive(page):
    lower = SearchPage(page).search_via_url("coffee")
    lower_count = lower.result_count()

    upper = SearchPage(page).search_via_url("COFFEE")
    upper_count = upper.result_count()

    assert lower_count == upper_count
    assert lower_count > 0


@pytest.mark.regression
@pytest.mark.search
@pytest.mark.parametrize("category", NAV_DATA["categories"], ids=[c["link_text"] for c in NAV_DATA["categories"]])
def test_category_navigation_from_header_menu(page, category):
    search_page = SearchPage(page)
    search_page.goto("/")

    search_page.header.go_to_category(category["link_text"])
    page.wait_for_timeout(1000)

    assert category["url_fragment"] in page.url
