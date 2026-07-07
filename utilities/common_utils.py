"""Generic helpers that don't fit a more specific utility module."""
import functools
import time
from datetime import datetime

from utilities.logger import get_logger

logger = get_logger(__name__)


def retry(times: int = 3, delay_seconds: float = 1.0, exceptions: tuple = (Exception,)):
    """Retry a flaky call (e.g. a network request) a fixed number of times."""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as exc:  # noqa: BLE001 - intentional broad retry
                    last_exc = exc
                    logger.warning(
                        "Attempt %d/%d for %s failed: %s", attempt, times, func.__name__, exc
                    )
                    if attempt < times:
                        time.sleep(delay_seconds)
            raise last_exc

        return wrapper

    return decorator


def timestamp(fmt: str = "%Y%m%d_%H%M%S") -> str:
    return datetime.now().strftime(fmt)


def extract_price_to_float(price_text: str) -> float:
    """Turn a rendered price like '₹2,499.00' into 2499.0."""
    cleaned = "".join(ch for ch in price_text if ch.isdigit() or ch == ".")
    return float(cleaned) if cleaned else 0.0
