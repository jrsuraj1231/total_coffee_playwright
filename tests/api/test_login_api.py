"""API tests around authentication boundaries on the public WordPress REST API.

total.coffee has no JWT/login REST endpoint, so "login" coverage at the
API layer means: proving anonymous requests only ever see public data and
can never perform a write/authenticated action.
"""
import json

import pytest

from api.endpoints import WP_ROOT, WP_USERS


@pytest.mark.api
def test_wp_json_root_lists_store_api_namespace(api_client):
    response = api_client.get(WP_ROOT)

    assert response.status == 200
    data = json.loads(response.text())
    assert "wc/store/v1" in data.get("namespaces", [])


@pytest.mark.api
def test_anonymous_users_list_exposes_only_public_fields(api_client):
    response = api_client.get(WP_USERS)

    assert response.status == 200
    users = json.loads(response.text())
    assert len(users) > 0

    sensitive_fields = {"email", "roles", "capabilities", "user_pass"}
    for user in users:
        assert not sensitive_fields.intersection(user.keys()), (
            f"Anonymous /wp/v2/users response leaked sensitive fields: {user.keys()}"
        )


@pytest.mark.api
def test_anonymous_user_creation_is_rejected(api_client):
    response = api_client.post(
        WP_USERS, data={"username": "automation_probe", "email": "probe@example.com", "password": "x"}
    )

    assert response.status == 401
    body = json.loads(response.text())
    assert body.get("code") == "rest_cannot_create_user"
