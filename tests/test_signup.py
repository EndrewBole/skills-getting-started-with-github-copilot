"""Tests for POST /activities/{activity_name}/signup endpoint."""


def test_signup_success(client, sample_activity_name, sample_email):
    """Test successful signup for an activity.
    
    Arrange: Test client, activity name, and new email
    Act: POST signup request with valid parameters
    Assert: Returns 200 with success message
    """
    # Arrange
    # (fixtures provide client, sample_activity_name, sample_email)
    
    # Act
    response = client.post(
        f"/activities/{sample_activity_name}/signup",
        params={"email": sample_email}
    )
    
    # Assert
    assert response.status_code == 200
    assert "message" in response.json()
    assert sample_email in response.json()["message"]


def test_signup_adds_participant(client, sample_activity_name, sample_email):
    """Test that signup actually adds participant to activity.
    
    Arrange: Test client, activity name, and new email
    Act: POST signup request, then GET activities
    Assert: Email appears in participants list
    """
    # Arrange
    # (fixtures provide client, sample_activity_name, sample_email)
    
    # Act
    client.post(
        f"/activities/{sample_activity_name}/signup",
        params={"email": sample_email}
    )
    response = client.get("/activities")
    data = response.json()
    participants = data[sample_activity_name]["participants"]
    
    # Assert
    assert sample_email in participants


def test_signup_nonexistent_activity_returns_404(client, sample_email):
    """Test signup for non-existent activity returns 404.
    
    Arrange: Test client with fake activity name
    Act: POST signup to non-existent activity
    Assert: Returns 404 with error detail
    """
    # Arrange
    fake_activity = "Nonexistent Activity"
    
    # Act
    response = client.post(
        f"/activities/{fake_activity}/signup",
        params={"email": sample_email}
    )
    
    # Assert
    assert response.status_code == 404
    assert "detail" in response.json()
    assert "not found" in response.json()["detail"].lower()


def test_signup_duplicate_email_returns_400(client, sample_activity_name, existing_email):
    """Test signup with already registered email returns 400.
    
    Arrange: Test client with existing participant email
    Act: POST signup with email already in activity
    Assert: Returns 400 with appropriate error
    """
    # Arrange
    # (existing_email is already in Basketball activity)
    
    # Act
    response = client.post(
        f"/activities/{sample_activity_name}/signup",
        params={"email": existing_email}
    )
    
    # Assert
    assert response.status_code == 400
    assert "detail" in response.json()
    assert "already signed up" in response.json()["detail"].lower()


def test_signup_without_email_param_returns_422(client, sample_activity_name):
    """Test signup without email parameter returns validation error.
    
    Arrange: Test client and activity name
    Act: POST signup without email query parameter
    Assert: Returns 422 validation error
    """
    # Arrange
    # (client and sample_activity_name from fixtures)
    
    # Act
    response = client.post(f"/activities/{sample_activity_name}/signup")
    
    # Assert
    assert response.status_code == 422


def test_signup_with_empty_email_returns_422(client, sample_activity_name):
    """Test signup with empty email parameter returns validation error.
    
    Arrange: Test client with empty email
    Act: POST signup with empty email string
    Assert: Returns 422 validation error
    """
    # Arrange
    empty_email = ""
    
    # Act
    response = client.post(
        f"/activities/{sample_activity_name}/signup",
        params={"email": empty_email}
    )
    
    # Assert
    assert response.status_code == 422


def test_signup_multiple_participants_same_activity(client, sample_activity_name):
    """Test multiple different participants can sign up for same activity.
    
    Arrange: Test client with multiple unique emails
    Act: POST signup for same activity with different emails
    Assert: All signups succeed and participants list grows
    """
    # Arrange
    emails = [
        "student1@mergington.edu",
        "student2@mergington.edu",
        "student3@mergington.edu"
    ]
    
    # Act
    for email in emails:
        response = client.post(
            f"/activities/{sample_activity_name}/signup",
            params={"email": email}
        )
        assert response.status_code == 200
    
    # Assert
    activities_response = client.get("/activities")
    participants = activities_response.json()[sample_activity_name]["participants"]
    for email in emails:
        assert email in participants


def test_signup_response_format(client, sample_activity_name, sample_email):
    """Test signup response has correct format.
    
    Arrange: Test client, activity, and email
    Act: POST successful signup
    Assert: Response contains message field with appropriate content
    """
    # Arrange
    # (fixtures provide client, sample_activity_name, sample_email)
    
    # Act
    response = client.post(
        f"/activities/{sample_activity_name}/signup",
        params={"email": sample_email}
    )
    data = response.json()
    
    # Assert
    assert "message" in data
    assert isinstance(data["message"], str)
    assert len(data["message"]) > 0
