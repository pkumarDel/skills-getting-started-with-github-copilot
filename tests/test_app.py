from fastapi.testclient import TestClient
from urllib.parse import quote

from src.app import app, activities


client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # basic sanity check for a known activity
    assert "Chess Club" in data


def test_signup_and_unregister_flow():
    activity = "Math Olympiad Club"
    email = "testuser@example.com"

    # Ensure a clean starting state for this test
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Sign up
    resp = client.post(f"/activities/{quote(activity, safe='')}/signup?email={email}")
    assert resp.status_code == 200
    assert email in activities[activity]["participants"]

    # Duplicate signup should fail
    resp = client.post(f"/activities/{quote(activity, safe='')}/signup?email={email}")
    assert resp.status_code == 400

    # Unregister
    resp = client.post(f"/activities/{quote(activity, safe='')}/unregister?email={email}")
    assert resp.status_code == 200
    assert email not in activities[activity]["participants"]

    # Unregistering again should fail
    resp = client.post(f"/activities/{quote(activity, safe='')}/unregister?email={email}")
    assert resp.status_code == 400
