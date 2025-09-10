import pytest

@pytest.mark.parametrize("endpoint", [
    "/api/admin/dashboard",
    "/api/admin/users",  
])
def test_admin_get_endpoints(admin_user, endpoint):
    client, token = admin_user
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get(endpoint, headers=headers)

    assert response.status_code == 200
    assert response.is_json


def test_admin_assign_missing_fields(admin_user):
    client, token = admin_user
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/api/admin/assign-caretaker", headers=headers, json={})

    assert response.status_code == 400
    assert response.get_json().get("error") == "senior_id and caretaker_id are required"


def test_admin_assign_invalid_ids(admin_user):
    client, token = admin_user
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"senior_id": 9999, "caretaker_id": 8888}  # non-existent IDs

    response = client.post("/api/admin/assign-caretaker", headers=headers, json=payload)
    assert response.status_code == 404
    assert "error" in response.get_json()
