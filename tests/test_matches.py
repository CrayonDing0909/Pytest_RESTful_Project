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
    """提供 FootballAPIClient 實例作為測試 fixture"""
    return FootballAPIClient(api_key=API_KEY)

@pytest.mark.parametrize(
    "date_from, date_to, api_key, status, expected_status, expected_matched_type, has_keys",
    parametrize_data,
    ids=ids
)
def test_get_matches(api_client, date_from, date_to, api_key, status, expected_status, expected_matched_type, has_keys):
    """
    測試案例：查詢比賽數據的多場景測試
    步驟：
    1. 使用指定的日期範圍、API Key 和狀態發送 GET 請求到 /v4/matches
    預期結果：見 test_data.json 中的 scenario 描述
    驗證方法：
    - 檢查狀態碼是否符合預期
    - 檢查 matches 和回應的類型
    - 檢查特定key是否存在
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