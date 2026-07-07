"""Locators for /my-account/ (login, register, lost-password) - confirmed against
the live total.coffee DOM (classic WooCommerce account forms, not block-based)."""


class LoginLocators:
    USERNAME_INPUT = "#username"
    PASSWORD_INPUT = "#password"
    REMEMBER_ME_CHECKBOX = "#rememberme"
    LOGIN_SUBMIT_BUTTON = "button[name='login']"
    LOGIN_ERROR_MESSAGE = ".woocommerce-error, .woocommerce-notices-wrapper .woocommerce-error"
    LOST_PASSWORD_LINK = "a:has-text('Lost your password?')"

    REGISTER_EMAIL_INPUT = "#reg_email"
    REGISTER_SUBMIT_BUTTON = "button[name='register']"
    REGISTER_ERROR_MESSAGE = ".woocommerce-error"

    ACCOUNT_LOGGED_IN_NAV = ".woocommerce-MyAccount-navigation"
    LOGOUT_LINK = ".woocommerce-MyAccount-navigation-link--customer-logout a"


class LostPasswordLocators:
    USER_LOGIN_INPUT = "#user_login"
    RESET_SUBMIT_BUTTON = "button:has-text('Reset password')"
    RESET_NOTICE = ".woocommerce-message, .woocommerce-error"
