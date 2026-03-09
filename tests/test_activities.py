"""Tests for GET /activities endpoint."""


def test_get_activities_returns_200(client):
    """Test that GET /activities returns successful response.
    
    Arrange: Test client is ready
    Act: Send GET request to /activities
    Assert: Response status is 200 OK
    """
    # Arrange
    # (client fixture provides the test client)
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200


def test_get_activities_returns_dict(client):
    """Test that GET /activities returns dictionary structure.
    
    Arrange: Test client is ready
    Act: Send GET request to /activities
    Assert: Response body is a dictionary
    """
    # Arrange
    # (client fixture provides the test client)
    
    # Act
    response = client.get("/activities")
    data = response.json()
    
    # Assert
    assert isinstance(data, dict)


def test_get_activities_returns_all_activities(client):
    """Test that GET /activities returns all 9 activities.
    
    Arrange: Test client with default activities
    Act: Send GET request to /activities
    Assert: Response contains exactly 9 activities
    """
    # Arrange
    expected_count = 9
    
    # Act
    response = client.get("/activities")
    data = response.json()
    
    # Assert
    assert len(data) == expected_count


def test_get_activities_contains_expected_activity(client, sample_activity_name):
    """Test that GET /activities includes Basketball activity.
    
    Arrange: Test client and sample activity name
    Act: Send GET request to /activities
    Assert: Basketball is in response keys
    """
    # Arrange
    # (fixtures provide client and sample_activity_name)
    
    # Act
    response = client.get("/activities")
    data = response.json()
    
    # Assert
    assert sample_activity_name in data


def test_activity_has_required_fields(client, sample_activity_name):
    """Test that each activity has required fields.
    
    Arrange: Test client and sample activity name
    Act: Get activities and extract sample activity
    Assert: Activity has description, schedule, max_participants, participants
    """
    # Arrange
    required_fields = ["description", "schedule", "max_participants", "participants"]
    
    # Act
    response = client.get("/activities")
    data = response.json()
    activity = data[sample_activity_name]
    
    # Assert
    for field in required_fields:
        assert field in activity


def test_activity_participants_is_list(client, sample_activity_name):
    """Test that participants field is a list.
    
    Arrange: Test client and sample activity name
    Act: Get activities and extract participants
    Assert: Participants is a list type
    """
    # Arrange
    # (fixtures provide client and sample_activity_name)
    
    # Act
    response = client.get("/activities")
    data = response.json()
    participants = data[sample_activity_name]["participants"]
    
    # Assert
    assert isinstance(participants, list)


def test_activity_max_participants_is_integer(client, sample_activity_name):
    """Test that max_participants field is an integer.
    
    Arrange: Test client and sample activity name
    Act: Get activities and extract max_participants
    Assert: max_participants is an integer
    """
    # Arrange
    # (fixtures provide client and sample_activity_name)
    
    # Act
    response = client.get("/activities")
    data = response.json()
    max_participants = data[sample_activity_name]["max_participants"]
    
    # Assert
    assert isinstance(max_participants, int)
    assert max_participants > 0
