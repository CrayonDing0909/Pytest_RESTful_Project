import requests

class FootballAPIClient:
    def __init__(self, api_key, base_url="https://api.football-data.org/v4"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {"X-Auth-Token": self.api_key}

    def get_matches(self, date_from=None, date_to=None, status=None):
        """
        查詢比賽數據
        :param date_from: 開始日期 (YYYY-MM-DD)
        :param date_to: 結束日期 (YYYY-MM-DD)
        :param status: 比賽狀態 (例如 LIVE, FINISHED)
        :return: requests.Response 物件
        """
        endpoint = f"{self.base_url}/matches"
        params = {}
        if date_from:
            params["dateFrom"] = date_from
        if date_to:
            params["dateTo"] = date_to
        if status:
            params["status"] = status
        
        try:
            response = requests.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            if 'response' not in locals():
                return requests.Response()
            return response