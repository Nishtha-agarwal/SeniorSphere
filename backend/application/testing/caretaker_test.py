import pytest
from datetime import datetime, timedelta, timezone

@pytest.mark.parametrize("endpoint", [
    "/api/caretaker/emergency",
    "/api/caretaker/sos_alerts",
    "/api/caretaker/missed_tasks",
    "/api/caretaker/unassigned",
])
def test_caretaker_read_only_endpoints(caretaker_user, endpoint):
    client, token = caretaker_user
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get(endpoint, headers=headers)

    assert response.status_code in [200, 404]  # 404 if no data
    if response.status_code == 200:
        assert response.is_json


def test_caretaker_add_routine_missing_fields(caretaker_user):
    client, token = caretaker_user
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/api/caretaker/add_routine", headers=headers, json={})



def test_caretaker_add_routine_invalid_senior(caretaker_user):
    client, token = caretaker_user
    headers = {"Authorization": f"Bearer {token}"}

    routine_payload = {
        "senior_id": 9999,  # invalid senior
        "task_details": "Check blood pressure",
        "duration": 15,
        "time": (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
    }

    response = client.post("/api/caretaker/add_routine", headers=headers, json=routine_payload)
    assert response.status_code == 404
    response_data  = response.get_json() or {}
