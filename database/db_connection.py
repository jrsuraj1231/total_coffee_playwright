"""Generic DB connection helper (SQLAlchemy), scaffolded for framework completeness.

total.coffee is a third-party hosted WooCommerce store - this framework
has no direct database credentials for it, so none of the 30 shipped
tests use this module. It's provided so a team with real DB access
(e.g. testing an internal staging clone) can drop in a connection string
via the DB_CONNECTION_STRING env var and start writing DB-validation
tests immediately, following the same pattern as api_client.py.
"""
import os

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker


def get_engine() -> Engine:
    conn_string = os.getenv("DB_CONNECTION_STRING")
    if not conn_string:
        raise EnvironmentError(
            "DB_CONNECTION_STRING is not set. This project has no real DB access to "
            "total.coffee; configure this only if pointing the framework at an "
            "internal database you control."
        )
    return create_engine(conn_string, pool_pre_ping=True)


def get_session():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()
