"""Generic helpers that don't fit a more specific utility module."""


def extract_price_to_float(price_text: str) -> float:
    """Turn a rendered price like '₹2,499.00' into 2499.0."""
    cleaned = "".join(ch for ch in price_text if ch.isdigit() or ch == ".")
    return float(cleaned) if cleaned else 0.0
