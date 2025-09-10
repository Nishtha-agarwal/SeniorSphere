import pytest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app import create_app

@pytest.fixture(scope="session")
def app():
    print("Create and configure app for testing")
    try:
        result = create_app()
        app = result[0]
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
     
        with app.app_context():
            yield app
            
    except Exception as e:
        pytest.fail(f"Failed to create app: {e}")
        

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture(scope="session")
def auth_user(app):   
    client = app.test_client()
    
    try:
        response = client.post("/api/login", json={
            "contact": "9876545676",
            "password": "1111"
        })
        
        if response.status_code != 200:
            error_msg = response.get_json() if response.get_json() else response.data
            pytest.fail(f"User login failed (Status: {response.status_code}): {error_msg}")
            
        token = response.get_json()["access_token"]
        yield client, token
        
    except KeyError as e:
        pytest.fail(f"Login response missing expected field: {e}")
    except Exception as e:
        pytest.fail(f"Authentication setup failed: {e}")


@pytest.fixture(scope="session")
def admin_user(app):  # Admin test user
    client = app.test_client()
    response = client.post("/api/login", json={
        "contact": "1234567890",
        "password": "9999999999"
    })
    if response.status_code != 200:
        pytest.fail(f"Admin login failed: {response.status_code} - {response.get_json()}")
    token = response.get_json()["access_token"]
    yield client, token


@pytest.fixture(scope="session")
def caretaker_user(app):  # Caretaker test user
    client = app.test_client()
    response = client.post("/api/login", json={
        "contact": "9876545676",
        "password": "1111"
    })
    if response.status_code != 200:
        pytest.fail(f"Caretaker login failed: {response.status_code} - {response.get_json()}")
    token = response.get_json()["access_token"]
    yield client, token