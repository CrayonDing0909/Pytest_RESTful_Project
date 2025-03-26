# api_client.py
import requests

class FootballAPIClient:
    def __init__(self, api_key, base_url="https://api.football-data.org/v4"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {"X-Auth-Token": self.api_key}

    def get_matches(self, date_from=None, date_to=None):
        endpoint = f"{self.base_url}/matches"
        params = {}
        if date_from:
            params["dateFrom"] = date_from
        if date_to:
            params["dateTo"] = date_to
        try:
            response = requests.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()  
            return response
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            if 'response' not in locals():
                return requests.Response()
            return response