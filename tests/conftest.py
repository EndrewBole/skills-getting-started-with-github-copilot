"""Pytest configuration and shared fixtures for backend tests."""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)


@pytest.fixture
def sample_activity_name():
    """Return a known activity name for testing."""
    return "Basketball"


@pytest.fixture
def sample_email():
    """Return a test email address."""
    return "test.student@mergington.edu"


@pytest.fixture
def existing_email():
    """Return an email that already exists in Basketball activity."""
    return "carlos@mergington.edu"


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities state before each test to ensure isolation."""
    # Store original state
    original_activities = {
        "Basketball": {
            "description": "Team sport focusing on basketball skills and competition",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["carlos@mergington.edu"]
        },
        "Tennis Club": {
            "description": "Learn tennis techniques and participate in matches",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:00 PM",
            "max_participants": 10,
            "participants": ["alex@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop argumentation and public speaking skills",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["jessica@mergington.edu", "james@mergington.edu"]
        },
        "Science Club": {
            "description": "Explore scientific concepts through experiments and projects",
            "schedule": "Fridays, 3:30 PM - 4:30 PM",
            "max_participants": 18,
            "participants": ["nora@mergington.edu"]
        },
        "Drama Club": {
            "description": "Act in theatrical productions and develop performance skills",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 25,
            "participants": ["lucas@mergington.edu", "sophia@mergington.edu"]
        },
        "Art Studio": {
            "description": "Create visual art through painting, drawing, and sculpture",
            "schedule": "Mondays and Wednesdays, 3:30 PM - 4:45 PM",
            "max_participants": 12,
            "participants": ["maya@mergington.edu"]
        },
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        }
    }
    
    # Reset activities to original state
    activities.clear()
    activities.update(original_activities)
    
    yield
    
    # Clean up after test (reset again)
    activities.clear()
    activities.update(original_activities)
