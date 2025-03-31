from api_client import FootballAPIClient
from config import API_KEY

#for check expected result is correct
def test_api_connection():
    client = FootballAPIClient(api_key=API_KEY)
    # 測試 1: invalid date
    response = client.get_matches(date_from="2024-13-01", date_to="2024-13-01")
    print(f"Invalid Date - Status Code: {response.status_code}")
    print(f"Invalid Date - Response: {response.json()}")
    
    # 測試 2: get data
    # can't exceed 10 day
    response = client.get_matches(date_from="2024-04-01", date_to="2024-04-10")
    print(f"LIVE Matches - Status Code: {response.status_code}")
    print(f"LIVE Matches - Response: {response.json()}")

if __name__ == "__main__":
    test_api_connection()