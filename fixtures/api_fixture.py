"""Pytest fixture providing an ApiClient bound to CONFIG.api_base_url."""
import pytest

from api.api_client import ApiClient
from config.config import CONFIG


@pytest.fixture
def api_client(playwright_instance) -> ApiClient:
    request_context = playwright_instance.request.new_context(
        base_url=CONFIG.api_base_url,
        extra_http_headers={"Content-Type": "application/json"},
    )
    client = ApiClient(request_context)
    yield client
    request_context.dispose()
