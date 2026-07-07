"""Thin wrapper around Playwright's APIRequestContext for the Store API.

Every method returns the raw APIResponse so tests can assert on status
code, headers, and body as needed. The client transparently keeps the
Nonce/Cart-Token pair in sync across calls so a GET -> POST -> GET
sequence behaves like a real browser session.
"""
from playwright.sync_api import APIRequestContext, APIResponse

from api.authentication import StoreApiSession
from utilities.logger import get_logger

logger = get_logger(__name__)


class ApiClient:
    def __init__(self, request_context: APIRequestContext):
        self.request_context = request_context
        self.session = StoreApiSession(request_context)

    def _headers(self, extra: dict | None = None) -> dict:
        headers = self.session.auth_headers()
        if extra:
            headers.update(extra)
        return headers

    def get(self, path: str, params: dict | None = None) -> APIResponse:
        logger.info("GET %s params=%s", path, params)
        response = self.request_context.get(path, params=params, headers=self._headers())
        self.session.capture_from_response(response)
        return response

    def post(self, path: str, data: dict | None = None) -> APIResponse:
        logger.info("POST %s data=%s", path, data)
        response = self.request_context.post(path, data=data, headers=self._headers())
        self.session.capture_from_response(response)
        return response

    def put(self, path: str, data: dict | None = None) -> APIResponse:
        logger.info("PUT %s data=%s", path, data)
        response = self.request_context.put(path, data=data, headers=self._headers())
        self.session.capture_from_response(response)
        return response

    def delete(self, path: str, data: dict | None = None) -> APIResponse:
        logger.info("DELETE %s data=%s", path, data)
        response = self.request_context.delete(path, data=data, headers=self._headers())
        self.session.capture_from_response(response)
        return response
