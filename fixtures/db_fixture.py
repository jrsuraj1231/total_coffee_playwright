"""Optional DB session fixture. Skips the test if DB_CONNECTION_STRING is not set,
since this framework has no real database access to the live total.coffee store."""
import os

import pytest


@pytest.fixture
def db_session():
    if not os.getenv("DB_CONNECTION_STRING"):
        pytest.skip("DB_CONNECTION_STRING not set - no DB access configured for this environment")

    from database.db_connection import get_session

    session = get_session()
    yield session
    session.close()
