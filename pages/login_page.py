"""Page Object for /my-account/ - login, register, lost-password forms
(classic WooCommerce shortcode markup, confirmed on the live site)."""
from playwright.sync_api import Page

from pages.base_page import BasePage


class LoginPage(BasePage):
    PATH = "/my-account/"

    USERNAME_INPUT = "#username"
    PASSWORD_INPUT = "#password"
    LOGIN_SUBMIT_BUTTON = "button[name='login']"
    LOGIN_ERROR_MESSAGE = ".woocommerce-error, .woocommerce-notices-wrapper .woocommerce-error"
    LOST_PASSWORD_LINK = "a:has-text('Lost your password?')"

    REGISTER_EMAIL_INPUT = "#reg_email"
    REGISTER_SUBMIT_BUTTON = "button[name='register']"
    REGISTER_ERROR_MESSAGE = ".woocommerce-error"

    ACCOUNT_LOGGED_IN_NAV = ".woocommerce-MyAccount-navigation"
    LOGOUT_LINK = ".woocommerce-MyAccount-navigation-link--customer-logout a"

    def __init__(self, page: Page):
        super().__init__(page)
        self.username_input = page.locator(self.USERNAME_INPUT)
        self.password_input = page.locator(self.PASSWORD_INPUT)
        self.login_button = page.locator(self.LOGIN_SUBMIT_BUTTON)
        self.login_error = page.locator(self.LOGIN_ERROR_MESSAGE)

        self.register_email_input = page.locator(self.REGISTER_EMAIL_INPUT)
        self.register_button = page.locator(self.REGISTER_SUBMIT_BUTTON)
        self.register_error = page.locator(self.REGISTER_ERROR_MESSAGE)

        self.account_nav = page.locator(self.ACCOUNT_LOGGED_IN_NAV)
        self.logout_link = page.locator(self.LOGOUT_LINK)

    def open(self) -> "LoginPage":
        self.goto(self.PATH)
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
        self.click(self.page.locator(self.LOST_PASSWORD_LINK))
        return LostPasswordPage(self.page)


class LostPasswordPage(BasePage):
    PATH = "/my-account/lost-password/"

    USER_LOGIN_INPUT = "#user_login"
    RESET_SUBMIT_BUTTON = "button:has-text('Reset password')"
    RESET_NOTICE = ".woocommerce-message, .woocommerce-error"

    def __init__(self, page: Page):
        super().__init__(page)
        self.user_login_input = page.locator(self.USER_LOGIN_INPUT)
        self.reset_button = page.locator(self.RESET_SUBMIT_BUTTON)
        self.notice = page.locator(self.RESET_NOTICE)

    def open(self) -> "LostPasswordPage":
        self.goto(self.PATH)
        return self

    def request_reset(self, username_or_email: str) -> None:
        self.fill(self.user_login_input, username_or_email)
        self.click(self.reset_button)

    def notice_text(self) -> str:
        return self.get_text(self.notice)
