"""Page Object for /my-account/ - login, register, lost-password forms
(classic WooCommerce shortcode markup, confirmed on the live site)."""
from playwright.sync_api import Page

from locators.login_locator import LoginLocators, LostPasswordLocators
from pages.base_page import BasePage
from resources.constants import PATH_LOST_PASSWORD, PATH_MY_ACCOUNT


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.username_input = page.locator(LoginLocators.USERNAME_INPUT)
        self.password_input = page.locator(LoginLocators.PASSWORD_INPUT)
        self.login_button = page.locator(LoginLocators.LOGIN_SUBMIT_BUTTON)
        self.login_error = page.locator(LoginLocators.LOGIN_ERROR_MESSAGE)

        self.register_email_input = page.locator(LoginLocators.REGISTER_EMAIL_INPUT)
        self.register_button = page.locator(LoginLocators.REGISTER_SUBMIT_BUTTON)
        self.register_error = page.locator(LoginLocators.REGISTER_ERROR_MESSAGE)

        self.account_nav = page.locator(LoginLocators.ACCOUNT_LOGGED_IN_NAV)
        self.logout_link = page.locator(LoginLocators.LOGOUT_LINK)

    def open(self) -> "LoginPage":
        self.goto(PATH_MY_ACCOUNT)
        return self

    def login(self, username: str, password: str) -> None:
        self.fill(self.username_input, username)
        self.fill(self.password_input, password)
        self.click(self.login_button)

    def is_login_error_visible(self) -> bool:
        return self.is_visible(self.login_error)

    def login_error_text(self) -> str:
        return self.get_text(self.login_error)

    def submit_registration(self, email: str) -> None:
        self.fill(self.register_email_input, email)
        self.click(self.register_button)

    def is_registered_successfully(self) -> bool:
        return self.is_visible(self.account_nav)

    def is_logged_in(self) -> bool:
        return self.is_visible(self.account_nav)

    def logout(self) -> None:
        self.click(self.logout_link)

    def open_lost_password(self) -> "LostPasswordPage":
        self.click(self.page.locator(LoginLocators.LOST_PASSWORD_LINK))
        return LostPasswordPage(self.page)


class LostPasswordPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.user_login_input = page.locator(LostPasswordLocators.USER_LOGIN_INPUT)
        self.reset_button = page.locator(LostPasswordLocators.RESET_SUBMIT_BUTTON)
        self.notice = page.locator(LostPasswordLocators.RESET_NOTICE)

    def open(self) -> "LostPasswordPage":
        self.goto(PATH_LOST_PASSWORD)
        return self

    def request_reset(self, username_or_email: str) -> None:
        self.fill(self.user_login_input, username_or_email)
        self.click(self.reset_button)

    def notice_text(self) -> str:
        return self.get_text(self.notice)
