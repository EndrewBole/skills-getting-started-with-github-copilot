"""Tests for DELETE /activities/{activity_name}/participants endpoint."""


def test_unregister_success(client, sample_activity_name, existing_email):
    """Test successful unregister of participant from activity.
    
    Arrange: Test client with activity containing existing participant
    Act: DELETE request to remove participant
    Assert: Returns 200 with success message
    """
    # Arrange
    # (existing_email is already in Basketball activity)
    
    # Act
    response = client.delete(
        f"/activities/{sample_activity_name}/participants",
        params={"email": existing_email}
    )
    
    # Assert
    assert response.status_code == 200
    assert "message" in response.json()
    assert existing_email in response.json()["message"]


def test_unregister_removes_participant(client, sample_activity_name, existing_email):
    """Test that unregister actually removes participant from activity.
    
    Arrange: Test client with existing participant
    Act: DELETE participant, then GET activities
    Assert: Email no longer in participants list
    """
    # Arrange
    # (existing_email is already in Basketball activity)
    
    # Act
    client.delete(
        f"/activities/{sample_activity_name}/participants",
        params={"email": existing_email}
    )
    response = client.get("/activities")
    data = response.json()
    participants = data[sample_activity_name]["participants"]
    
    # Assert
    assert existing_email not in participants


def test_unregister_nonexistent_activity_returns_404(client, sample_email):
    """Test unregister from non-existent activity returns 404.
    
    Arrange: Test client with fake activity name
    Act: DELETE request to non-existent activity
    Assert: Returns 404 with error detail
    """
    # Arrange
    fake_activity = "Nonexistent Activity"
    
    # Act
    response = client.delete(
        f"/activities/{fake_activity}/participants",
        params={"email": sample_email}
    )
    
    # Assert
    assert response.status_code == 404
    assert "detail" in response.json()
    assert "not found" in response.json()["detail"].lower()


def test_unregister_nonexistent_participant_returns_404(client, sample_activity_name, sample_email):
    """Test unregister of non-registered participant returns 404.
    
    Arrange: Test client with email not in activity
    Act: DELETE request for participant not in activity
    Assert: Returns 404 with error detail
    """
    # Arrange
    # (sample_email is not registered in Basketball activity)
    
    # Act
    response = client.delete(
        f"/activities/{sample_activity_name}/participants",
        params={"email": sample_email}
    )
    
    # Assert
    assert response.status_code == 404
    assert "detail" in response.json()
    assert "not found" in response.json()["detail"].lower()


def test_unregister_without_email_param_returns_422(client, sample_activity_name):
    """Test unregister without email parameter returns validation error.
    
    Arrange: Test client and activity name
    Act: DELETE request without email query parameter
    Assert: Returns 422 validation error
    """
    # Arrange
    # (client and sample_activity_name from fixtures)
    
    # Act
    response = client.delete(f"/activities/{sample_activity_name}/participants")
    
    # Assert
    assert response.status_code == 422


def test_unregister_with_empty_email_returns_422(client, sample_activity_name):
    """Test unregister with empty email parameter returns validation error.
    
    Arrange: Test client with empty email
    Act: DELETE request with empty email string
    Assert: Returns 422 validation error
    """
    # Arrange
    empty_email = ""
    
    # Act
    response = client.delete(
        f"/activities/{sample_activity_name}/participants",
        params={"email": empty_email}
    )
    
    # Assert
    assert response.status_code == 422


def test_unregister_decrements_participant_count(client, sample_activity_name, existing_email):
    """Test that unregister decreases participant count by one.
    
    Arrange: Get initial participant count
    Act: DELETE participant
    Assert: Participant count decreased by 1
    """
    # Arrange
    initial_response = client.get("/activities")
    initial_count = len(initial_response.json()[sample_activity_name]["participants"])
    
    # Act
    client.delete(
        f"/activities/{sample_activity_name}/participants",
        params={"email": existing_email}
    )
    
    # Assert
    final_response = client.get("/activities")
    final_count = len(final_response.json()[sample_activity_name]["participants"])
    assert final_count == initial_count - 1


def test_unregister_response_format(client, sample_activity_name, existing_email):
    """Test unregister response has correct format.
    
    Arrange: Test client with existing participant
    Act: DELETE successful unregister
    Assert: Response contains message field with appropriate content
    """
    # Arrange
    # (fixtures provide client, sample_activity_name, existing_email)
    
    # Act
    response = client.delete(
        f"/activities/{sample_activity_name}/participants",
        params={"email": existing_email}
    )
    data = response.json()
    
    # Assert
    assert "message" in data
    assert isinstance(data["message"], str)
    assert len(data["message"]) > 0


def test_unregister_allows_re_signup(client, sample_activity_name, existing_email):
    """Test that after unregister, same email can sign up again.
    
    Arrange: Test client with existing participant
    Act: DELETE participant, then signup same email
    Assert: Both operations succeed
    """
    # Arrange
    # (existing_email is already in Basketball activity)
    
    # Act
    unregister_response = client.delete(
        f"/activities/{sample_activity_name}/participants",
        params={"email": existing_email}
    )
    signup_response = client.post(
        f"/activities/{sample_activity_name}/signup",
        params={"email": existing_email}
    )
    
    # Assert
    assert unregister_response.status_code == 200
    assert signup_response.status_code == 200
    
    # Verify participant is back in the list
    activities_response = client.get("/activities")
    participants = activities_response.json()[sample_activity_name]["participants"]
    assert existing_email in participants
