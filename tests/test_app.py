import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_success():
    activity = "Soccer Team"
    email = "test_student@mergington.edu"
    # Ensure clean state
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    assert email in activities[activity]["participants"]
    assert resp.json()["message"] == f"Signed up {email} for {activity}"


def test_signup_duplicate():
    activity = "Soccer Team"
    email = "duplicate@mergington.edu"
    # Ensure participant exists
    if email not in activities[activity]["participants"]:
        activities[activity]["participants"].append(email)

    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 400


def test_signup_not_found():
    resp = client.post("/activities/Nonexistent/signup?email=foo@bar.com")
    assert resp.status_code == 404
