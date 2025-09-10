import io
import pytest

def make_pdf_file():
    """Create an in-memory fake PDF file."""
    return io.BytesIO(b"%PDF-1.4\nFake PDF content\n%%EOF")


def test_caretaker_register_success(client):
    """Register a caretaker successfully with all required fields and a PDF resume."""
    data = {
        "email": "caretaker@example.com",
        "password": "securePass123",
        "fullName": "John Doe",
        "age": "30",
        "contact": "9876543210",
        "qualifications": "B.Sc Nursing",
        "languages": "English,Hindi",
        "about": "Experienced caretaker"
    }
    # make a sample PDF file
    data["resume"] = (make_pdf_file(), "resume.pdf")

    response = client.post(
        "/api/register/caretaker",
        data=data,
        content_type="multipart/form-data"
    )

    assert response.status_code == 201
    resp_json = response.get_json()
    assert resp_json.get("message") == "Caretaker registered successfully"


def test_caretaker_register_missing_fields(client):
    """Missing required fields should return 400 with error message."""
    data = {
    "email": "caretaker3@example.com",
    "password": "SuperSecure789",
    "fullName": "David Williams",
    "age": "35",
    "contact": "9090887766",
    "qualifications": "Certified Caregiver",
    "languages": "English,Marathi",
    "about": "Dedicated caretaker with 5+ years of experience in senior care and emergency handling."
}
# Attach resume as PDF
    data["resume"] = (make_pdf_file(), "resume.pdf")

    response = client.post(
        "/api/register/caretaker",
        data=data
    )

    assert response.status_code == 400
    resp_json = response.get_json()
    assert resp_json.get("error") == "Missing required fields"


def test_senior_register_success(client):
    """Register a senior citizen successfully with full valid data."""
    payload = {
    "fullName": "Sophia Brown",
    "age": 72,
    "password": "safePass7",
    "contact": "9191919191",
    "languages": "English,Hindi",
    "pinCode": "400001",
    "city": "Mumbai",
    "state": "Maharashtra",
    "emergencyContact": "9988776655",
    "emergencyContactName": "Emily Brown",
    "emergencyEmail": "emergency2@example.com"
}

    

    response = client.post("/api/register/senior", json=payload)

    assert response.status_code == 201
    resp_json = response.get_json()
    assert resp_json.get("message") == "Senior Citizen registered successfully"


def test_senior_register_missing_fields(client):
    """Missing required fields should return 400 and errors list."""
    payload = {
        "fullName": "",
        "age": "",
        "password": "",
        "contact": "",
        "languages": "",
        "pinCode": "",
        "city": "",
        "state": "",
        "emergencyContact": "",
        "emergencyContactName": "",
    }

    response = client.post("/api/register/senior", json=payload)
    assert response.status_code == 400
    resp_json = response.get_json()
    assert "errors" in resp_json
    assert len(resp_json["errors"]) > 0


@pytest.mark.parametrize("login_payload, expected_status, expected_message", [
    ({"contact": "1234567890", "password": "9999999999"}, 200, "Login successful"),  # Admin
    ({"contact": "1234567890", "password": "wrongpass"}, 401, "Invalid contact or password."),  # Wrong pass
    ({"contact": "9876543210", "password": "securePass123"}, 200, "Login successful"),  # Caretaker
    ({"contact": "9123456789", "password": "myPass"}, 200, "Login successful"),  # Senior
])
def test_login(client, login_payload, expected_status, expected_message):
    response = client.post("/api/login", json=login_payload)
    assert response.status_code == expected_status
    resp_json = response.get_json()
    if expected_status == 200:
        assert resp_json.get("message") == expected_message
        assert "access_token" in resp_json
    else:
        assert resp_json.get("error") == expected_message
