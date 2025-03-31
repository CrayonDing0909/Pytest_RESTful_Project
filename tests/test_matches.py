import pytest
import json
from api_client import FootballAPIClient
from config import API_KEY

# loading test data
with open("test_data.json", "r") as f:
    TEST_DATA = json.load(f)

# 轉換成 parametrize 需要的格式
parametrize_data = [
    (
        case["date_from"],
        case["date_to"],
        API_KEY if case["api_key"] == "API_KEY" else case["api_key"],
        case["status"],
        case["expected_status"],
        list if case["expected_matched_type"] == "list" else dict,
        case["has_keys"]
    )
    for case in TEST_DATA
]

# 使用 scenario 作為測試名稱
ids = [case["scenario"] for case in TEST_DATA]

@pytest.fixture
def api_client():
    return FootballAPIClient(api_key=API_KEY)

@pytest.mark.parametrize(
    "date_from, date_to, api_key, status, expected_status, expected_matched_type, has_keys",
    parametrize_data,
    ids=ids
)
def test_get_matches(api_client, date_from, date_to, api_key, status, expected_status, expected_matched_type, has_keys):
    """
    Test Case:

    Steps:  
    1. Load test data from `test_data.json`, including date range (`date_from`, `date_to`), API Key (`api_key`), and match status (`status`).  
    2. Use `FootballAPIClient` to send a GET request to the `/v4/matches` endpoint for each test case:  
    - **Positive Cases**: Query past or live match data.  
    - **Negative Cases**: Test invalid API Key or incorrect date format.  
    - **Edge Cases**: Query future dates.

    Expected Results:  
    - **Positive Cases (Past Matches, Live Matches)**: Status code **200**, `matches` is a list of match data (can be empty). If data exists, it includes specific keys (e.g., `homeTeam`, `score`).  
    - **Negative Cases (Invalid API Key, Invalid Date Format)**: Status code **400**, response is an error dictionary containing the `message` key.  
    Detailed results are described in `test_data.json` under the `scenario` section.  

    Verification Method:  
    - **Check Status Code**: Use `assert response.status_code == expected_status` to ensure the API returns the expected status (**200** for success, **400** for errors).  
    - **Check Response Type**:  
    - If status code is not **200** (Negative Cases), use `isinstance(response_data, expected_matched_type)` to confirm the response is a dictionary.  
    - If status code is **200** (Positive & Edge Cases), use `isinstance(response_data["matches"], expected_matched_type)` to confirm `matches` is a list.  
    - **Check Specific Keys**: Use `all(key in data for key in has_keys)` to verify expected keys exist:  
    - **Positive Cases**: Check match data keys (e.g., `homeTeam`, `score`) to ensure data completeness.  
    - **Negative Cases**: Check for the error message key (`message`) to confirm readable errors.  
    """
    client = FootballAPIClient(api_key=api_key)
    response = client.get_matches(date_from=date_from, date_to=date_to, status=status)
    
    assert response.status_code == expected_status, f"Expected status {expected_status}, got {response.status_code}" #驗證status code expecteds
    response_data = response.json()
    
    if expected_status != 200:
        assert isinstance(response_data, expected_matched_type), f"Expected response type {expected_matched_type}"
        assert all(key in response_data for key in has_keys), f"Expected keys {has_keys} in response"
    else:
        assert isinstance(response_data["matches"], expected_matched_type), f"Expected matches type {expected_matched_type}"
        if has_keys and response_data["matches"]:
            assert all(key in response_data["matches"][0] for key in has_keys), f"Expected keys {has_keys} in matches"