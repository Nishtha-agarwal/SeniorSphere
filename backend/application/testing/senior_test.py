import pytest

def test_protected_endpoint(auth_user):
    client, token = auth_user
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/api/senior", headers=headers)
    
    assert response.status_code == 200
    data = response.get_json()
    assert data is not None, "Response should contain JSON data"



def test_senior_routine_tasks(auth_user):
    client, token = auth_user
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/senior/routine", headers=headers)
    assert response.status_code == 200


def test_senior_sos_post(auth_user):
    client, token = auth_user
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/api/senior/sos", headers=headers)
    assert response.status_code == 201
    data = response.get_json()
    assert data.get("message") == "SOS alert sent successfully"


def test_senior_get_query(auth_user):
    client, token = auth_user
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/senior/query", headers=headers)
    assert response.status_code == 200



@pytest.mark.parametrize("payload, expected_status, expected_response", [
    ({"message": "Need assistance with medication."}, 201, {"message": "Query raised successfully"}),
    ({"message": ""}, 400, {"error": "Message cannot be blank"}),
    ({}, 400, {"error": "Message cannot be blank"}), 
])
def test_senior_post_query(auth_user, payload, expected_status, expected_response):
    client, token = auth_user
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/api/senior/query", headers=headers, json=payload)

    assert response.status_code == expected_status
    data = response.get_json()
    for key, value in expected_response.items():
        assert data.get(key) == value
