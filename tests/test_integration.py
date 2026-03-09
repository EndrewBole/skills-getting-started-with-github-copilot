"""Integration tests for end-to-end workflows involving multiple endpoints."""


def test_complete_signup_and_list_workflow(client, sample_activity_name, sample_email):
    """Test complete workflow: signup -> list activities -> verify participant.
    
    Arrange: Test client with new email
    Act: Sign up for activity, then get activities list
    Assert: Participant appears in activity with updated count
    """
    # Arrange
    # Get initial state
    initial_response = client.get("/activities")
    initial_participants = initial_response.json()[sample_activity_name]["participants"]
    initial_count = len(initial_participants)
    
    # Act
    # Step 1: Signup
    signup_response = client.post(
        f"/activities/{sample_activity_name}/signup",
        params={"email": sample_email}
    )
    
    # Step 2: List activities
    list_response = client.get("/activities")
    final_participants = list_response.json()[sample_activity_name]["participants"]
    
    # Assert
    assert signup_response.status_code == 200
    assert list_response.status_code == 200
    assert sample_email in final_participants
    assert len(final_participants) == initial_count + 1


def test_signup_unregister_workflow(client, sample_activity_name, sample_email):
    """Test workflow: signup -> verify -> unregister -> verify removal.
    
    Arrange: Test client with new email
    Act: Sign up, verify participant, unregister, verify removal
    Assert: All steps succeed with correct state changes
    """
    # Arrange
    # (fixtures provide client, sample_activity_name, sample_email)
    
    # Act
    # Step 1: Signup
    signup_response = client.post(
        f"/activities/{sample_activity_name}/signup",
        params={"email": sample_email}
    )
    
    # Step 2: Verify signup
    after_signup = client.get("/activities")
    participants_after_signup = after_signup.json()[sample_activity_name]["participants"]
    
    # Step 3: Unregister
    unregister_response = client.delete(
        f"/activities/{sample_activity_name}/participants",
        params={"email": sample_email}
    )
    
    # Step 4: Verify removal
    after_unregister = client.get("/activities")
    participants_after_unregister = after_unregister.json()[sample_activity_name]["participants"]
    
    # Assert
    assert signup_response.status_code == 200
    assert sample_email in participants_after_signup
    assert unregister_response.status_code == 200
    assert sample_email not in participants_after_unregister


def test_multiple_signups_different_activities(client):
    """Test one participant signing up for multiple different activities.
    
    Arrange: Test client with email and multiple activity names
    Act: Sign up same email for different activities
    Assert: Email appears in all selected activities
    """
    # Arrange
    email = "multi.activity@mergington.edu"
    activities_to_join = ["Basketball", "Tennis Club", "Chess Club"]
    
    # Act
    for activity in activities_to_join:
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        assert response.status_code == 200
    
    # Assert
    all_activities = client.get("/activities").json()
    for activity in activities_to_join:
        assert email in all_activities[activity]["participants"]


def test_multiple_participants_same_activity_workflow(client, sample_activity_name):
    """Test multiple participants joining same activity in sequence.
    
    Arrange: Test client with list of unique emails
    Act: Sign up each email sequentially
    Assert: All participants appear in activity list
    """
    # Arrange
    emails = [
        "participant1@mergington.edu",
        "participant2@mergington.edu",
        "participant3@mergington.edu",
        "participant4@mergington.edu"
    ]
    
    # Act
    for email in emails:
        response = client.post(
            f"/activities/{sample_activity_name}/signup",
            params={"email": email}
        )
        assert response.status_code == 200
    
    # Assert
    activities = client.get("/activities").json()
    participants = activities[sample_activity_name]["participants"]
    for email in emails:
        assert email in participants


def test_signup_unregister_re_signup_workflow(client, sample_activity_name, sample_email):
    """Test workflow: signup -> unregister -> signup again.
    
    Arrange: Test client with new email
    Act: Complete signup cycle, unregister, then signup again
    Assert: All operations succeed and final state shows participant
    """
    # Arrange
    # (fixtures provide client, sample_activity_name, sample_email)
    
    # Act
    # Step 1: Initial signup
    signup1 = client.post(
        f"/activities/{sample_activity_name}/signup",
        params={"email": sample_email}
    )
    
    # Step 2: Unregister
    unregister = client.delete(
        f"/activities/{sample_activity_name}/participants",
        params={"email": sample_email}
    )
    
    # Step 3: Signup again
    signup2 = client.post(
        f"/activities/{sample_activity_name}/signup",
        params={"email": sample_email}
    )
    
    # Step 4: Verify final state
    final_state = client.get("/activities")
    participants = final_state.json()[sample_activity_name]["participants"]
    
    # Assert
    assert signup1.status_code == 200
    assert unregister.status_code == 200
    assert signup2.status_code == 200
    assert sample_email in participants


def test_partial_unregister_workflow(client, sample_activity_name):
    """Test unregistering some but not all participants from activity.
    
    Arrange: Add multiple participants to activity
    Act: Unregister only some participants
    Assert: Correct participants remain and removed ones are gone
    """
    # Arrange
    emails_to_add = [
        "temp1@mergington.edu",
        "temp2@mergington.edu",
        "temp3@mergington.edu"
    ]
    emails_to_remove = ["temp1@mergington.edu", "temp3@mergington.edu"]
    emails_to_keep = ["temp2@mergington.edu"]
    
    # Add all participants
    for email in emails_to_add:
        client.post(
            f"/activities/{sample_activity_name}/signup",
            params={"email": email}
        )
    
    # Act
    # Remove some participants
    for email in emails_to_remove:
        response = client.delete(
            f"/activities/{sample_activity_name}/participants",
            params={"email": email}
        )
        assert response.status_code == 200
    
    # Assert
    final_activities = client.get("/activities").json()
    participants = final_activities[sample_activity_name]["participants"]
    
    # Removed participants should not be present
    for email in emails_to_remove:
        assert email not in participants
    
    # Kept participants should still be present
    for email in emails_to_keep:
        assert email in participants


def test_error_recovery_workflow(client, sample_activity_name, sample_email):
    """Test that failed operations don't corrupt state.
    
    Arrange: Test client with valid email
    Act: Attempt invalid operation, then valid operation
    Assert: Valid operation succeeds despite previous error
    """
    # Arrange
    # (fixtures provide client, sample_activity_name, sample_email)
    
    # Act
    # Step 1: Try to signup to non-existent activity (should fail)
    failed_signup = client.post(
        "/activities/FakeActivity/signup",
        params={"email": sample_email}
    )
    
    # Step 2: Valid signup should still work
    valid_signup = client.post(
        f"/activities/{sample_activity_name}/signup",
        params={"email": sample_email}
    )
    
    # Step 3: Try to unregister from non-existent activity (should fail)
    failed_unregister = client.delete(
        "/activities/FakeActivity/participants",
        params={"email": sample_email}
    )
    
    # Step 4: Valid unregister should still work
    valid_unregister = client.delete(
        f"/activities/{sample_activity_name}/participants",
        params={"email": sample_email}
    )
    
    # Assert
    assert failed_signup.status_code == 404
    assert valid_signup.status_code == 200
    assert failed_unregister.status_code == 404
    assert valid_unregister.status_code == 200


def test_participant_count_consistency_workflow(client, sample_activity_name):
    """Test participant count remains consistent through signup/unregister cycles.
    
    Arrange: Get initial participant count
    Act: Perform multiple signups and unregisters
    Assert: Final count matches expected based on operations
    """
    # Arrange
    initial_response = client.get("/activities")
    initial_count = len(initial_response.json()[sample_activity_name]["participants"])
    
    emails = [
        "counter1@mergington.edu",
        "counter2@mergington.edu",
        "counter3@mergington.edu"
    ]
    
    # Act
    # Add 3 participants
    for email in emails:
        client.post(
            f"/activities/{sample_activity_name}/signup",
            params={"email": email}
        )
    
    # Remove 1 participant
    client.delete(
        f"/activities/{sample_activity_name}/participants",
        params={"email": emails[1]}
    )
    
    # Assert
    final_response = client.get("/activities")
    final_count = len(final_response.json()[sample_activity_name]["participants"])
    
    # Should be initial + 3 - 1 = initial + 2
    assert final_count == initial_count + 2
