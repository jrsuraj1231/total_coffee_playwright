"""Helpers for resolving the active test environment."""
import os

DEFAULT_ENV = "qa"


def get_current_env() -> str:
    return os.getenv("ENV", DEFAULT_ENV).strip().lower()


def is_production() -> bool:
    """total.coffee is a live public store in every configured environment.

    Destructive flows (placing real orders, submitting real registrations,
    sending real contact-form emails) must never run regardless of ENV.
    Tests should check this helper before doing anything with a real
    side-effect on the live business.
    """
    return True
