"""Random test-data generation backed by Faker, for negative/registration tests.

Never used to actually submit real registrations against total.coffee -
only to build invalid/edge-case payloads for client-side validation tests.
"""
import random
import string

from faker import Faker

fake = Faker()


def random_email() -> str:
    return fake.unique.email()


def random_invalid_email() -> str:
    return f"not-an-email-{random.randint(1000, 9999)}"


def random_name() -> str:
    return fake.name()


def random_phone() -> str:
    return fake.msisdn()[:10]


def random_password(length: int = 12) -> str:
    alphabet = string.ascii_letters + string.digits + "!@#$%"
    return "".join(random.choice(alphabet) for _ in range(length))


def random_search_term() -> str:
    return random.choice(["coffee", "grinder", "filter", "kettle", "dripper"])


def random_string(length: int = 8) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=length))
