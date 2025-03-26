from api_client import FootballAPIClient
from config import API_KEY

def test_api_connection():
    client = FootballAPIClient(api_key=API_KEY)
    response = client.get_matches(date_from="2025-03-26", date_to="2025-03-26")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

if __name__ == "__main__":
    test_api_connection()