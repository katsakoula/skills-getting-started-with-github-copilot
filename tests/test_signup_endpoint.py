import src.app as app_module


def test_signup_successfully_adds_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "new.student@mergington.edu"
    endpoint = f"/activities/{activity}/signup?email={email}"

    # Act
    response = client.post(endpoint)
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert payload["message"] == f"Signed up {email} for {activity}"
    assert email in app_module.activities[activity]["participants"]


def test_signup_returns_404_for_unknown_activity(client):
    # Arrange
    endpoint = "/activities/Unknown%20Club/signup?email=student@mergington.edu"

    # Act
    response = client.post(endpoint)
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Activity not found"


def test_signup_returns_400_for_duplicate_registration(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"
    endpoint = f"/activities/{activity}/signup?email={email}"

    # Act
    response = client.post(endpoint)
    payload = response.json()

    # Assert
    assert response.status_code == 400
    assert payload["detail"] == "Student already signed up"


def test_signup_returns_400_when_activity_is_full(client):
    # Arrange
    activity = "Chess Club"
    max_participants = app_module.activities[activity]["max_participants"]
    app_module.activities[activity]["participants"] = [
        f"student{i}@mergington.edu" for i in range(max_participants)
    ]
    endpoint = f"/activities/{activity}/signup?email=overflow@mergington.edu"

    # Act
    response = client.post(endpoint)
    payload = response.json()

    # Assert
    assert response.status_code == 400
    assert payload["detail"] == "Activity is full"


def test_signup_returns_422_when_email_is_missing(client):
    # Arrange
    endpoint = "/activities/Chess%20Club/signup"

    # Act
    response = client.post(endpoint)

    # Assert
    assert response.status_code == 422
