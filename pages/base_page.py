"""Base Page Object: common navigation/interaction wrappers used by every page."""
from playwright.sync_api import Locator, Page

from components.popup import Popup
from config.config import CONFIG
from utilities.logger import get_logger

logger = get_logger(__name__)


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.popup = Popup(page)

    def goto(self, path: str, dismiss_popup: bool = True) -> None:
        url = path if path.startswith("http") else f"{CONFIG.base_url}{path}"
        logger.info("Navigating to %s", url)
        self.page.goto(url)
        if dismiss_popup:
            self.popup.dismiss_if_present(timeout=2000)

    def click(self, locator: Locator) -> None:
        locator.first.click()

    def fill(self, locator: Locator, value: str) -> None:
        locator.first.fill(value)

    def get_text(self, locator: Locator) -> str:
        return (locator.first.text_content() or "").strip()

    def is_visible(self, locator: Locator, timeout: int = 5000) -> bool:
        try:
            return locator.first.is_visible(timeout=timeout)
        except Exception:
            return False

    def title(self) -> str:
        return self.page.title()

    def current_url(self) -> str:
        return self.page.url

    def reload(self) -> None:
        self.page.reload()
