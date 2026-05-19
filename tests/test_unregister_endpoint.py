import src.app as app_module


def test_unregister_successfully_removes_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"
    endpoint = f"/activities/{activity}/participants?email={email}"

    # Act
    response = client.delete(endpoint)
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert payload["message"] == f"Unregistered {email} from {activity}"
    assert email not in app_module.activities[activity]["participants"]


def test_unregister_returns_404_for_unknown_activity(client):
    # Arrange
    endpoint = "/activities/Unknown%20Club/participants?email=student@mergington.edu"

    # Act
    response = client.delete(endpoint)
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Activity not found"


def test_unregister_returns_404_for_non_registered_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "not.registered@mergington.edu"
    endpoint = f"/activities/{activity}/participants?email={email}"

    # Act
    response = client.delete(endpoint)
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Student not registered for this activity"


def test_unregister_returns_422_when_email_is_missing(client):
    # Arrange
    endpoint = "/activities/Chess%20Club/participants"

    # Act
    response = client.delete(endpoint)

    # Assert
    assert response.status_code == 422
