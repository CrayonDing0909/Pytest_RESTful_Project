import pytest
from api_client import FootBallApiClient
from config import API_KEY

@pytest.fixture
def api_client():
    return FootBallApiClient(API_KEY)

def test_get_matches(api_client):
    matches = api_client.get_matches(date_from="2025-03-25", date_to="2025-03-25")