"""Site footer component: policy links, order tracking, contact, subscribe."""
from playwright.sync_api import Page


class Footer:
    def __init__(self, page: Page):
        self.page = page
        self.about_us_link = page.get_by_role("link", name="About Us")
        self.faq_link = page.get_by_role("link", name="FAQs")
        self.privacy_policy_link = page.get_by_role("link", name="Privacy Policy")
        self.terms_link = page.get_by_role("link", name="Terms & Conditions")
        self.order_tracking_link = page.get_by_role("link", name="Order Tracking")
        self.contact_us_link = page.get_by_role("link", name="Contact Us")

    def scroll_into_view(self) -> None:
        self.about_us_link.scroll_into_view_if_needed()

    def go_to_order_tracking(self) -> None:
        self.order_tracking_link.click()
