"""Compare UI/API observed values against DB rows (see db_connection.py)."""
from sqlalchemy import text
from sqlalchemy.orm import Session


def fetch_one(session: Session, query: str, params: dict) -> dict | None:
    result = session.execute(text(query), params).mappings().first()
    return dict(result) if result else None


def assert_order_status_matches(session: Session, order_id: int, expected_status: str) -> None:
    from database.queries import GET_ORDER_STATUS

    row = fetch_one(session, GET_ORDER_STATUS, {"order_id": order_id})
    assert row is not None, f"No order found with id {order_id}"
    assert row["status"] == expected_status, f"Expected status {expected_status}, got {row['status']}"
