# AAA-style tests for the FastAPI activities endpoints

def test_get_activities(client):
    # Arrange: fixtures provide initial state
    # Act
    resp = client.get("/activities")
    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_success(client):
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    # Act
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert resp.status_code == 200
    assert f"Signed up {email}" in resp.json().get("message", "")
    # verify added
    resp2 = client.get("/activities")
    assert email in resp2.json()[activity]["participants"]


def test_signup_duplicate(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"  # already present
    # Act
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert resp.status_code == 400
    assert resp.json().get("detail") == "Student already signed up for this activity"


def test_delete_participant_success(client):
    # Arrange
    activity = "Chess Club"
    email = "tempremover@mergington.edu"
    # add participant first
    add = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert add.status_code == 200
    # Act
    resp = client.delete(f"/activities/{activity}/participants", params={"email": email})
    # Assert
    assert resp.status_code == 200
    assert f"Removed {email}" in resp.json().get("message", "")
    # verify removed
    resp2 = client.get("/activities")
    assert email not in resp2.json()[activity]["participants"]


def test_delete_participant_not_found(client):
    # Arrange
    activity = "Chess Club"
    email = "noone@mergington.edu"
    # Act
    resp = client.delete(f"/activities/{activity}/participants", params={"email": email})
    # Assert
    assert resp.status_code == 404
    assert resp.json().get("detail") == "Participant not found"
