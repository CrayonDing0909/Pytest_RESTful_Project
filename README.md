# Football API Tests

This project tests the Football-Data.org API (`/v4/matches` endpoint) using Python and Pytest, designed for OpenNet's home test. It focuses on sports betting scenarios relevant to SportyBet, such as match data retrieval and error handling.

## Test Cases

| Test Case                   | Steps                                              | Expected Result                        | Validation Method                          |
|-----------------------------|----------------------------------------------------|----------------------------------------|--------------------------------------------|
| Positive - Query past matches | Send GET with 2024-03-16 to 2024-03-20            | Status 200, matches list with data     | Check status, matches type, keys (homeTeam, score) |
| Negative - Invalid API Key  | Send GET with invalid key                         | Status 400, error message              | Check status, response type, message key   |
| Boundary - Future date      | Send GET with 2025-03-26                         | Status 200, empty matches list         | Check status, matches is empty list        |
| Negative - Invalid date format | Send GET with 2024-13-01                        | Status 400, error message              | Check status, response type, message key   |
| Positive - Query live matches | Send GET with 2024-03-26, status=LIVE            | Status 200, matches list (may be empty)| Check status, matches type                 |

## Validation Explanation
- **Status Code**: Verified with `assert response.status_code == expected_status` to confirm API success or error handling, as it’s the primary indicator of request outcome.
- **Response Type**: Checked with `isinstance()` to ensure `matches` is a list (for 200 responses) or response is a dict (for 400 errors), aligning with API documentation.
- **Key Presence**: Validated with `all(key in data for key in has_keys)` to ensure critical data (e.g., homeTeam, score) or error details (message) are present, crucial for sports betting applications.

## Design Notes
- **Modularity**: API logic (`api_client.py`), tests (`test_matches.py`), and config (`config.py`) are separated for maintainability.
- **Data-Driven Testing**: Test data is stored in `test_data.json` with a `"scenario"` field for better readability and maintenance, separating data from logic.
- **Pytest Parametrize**: Used to reduce code duplication while covering multiple scenarios (positive, negative, boundary), meeting the requirement for high coverage.

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Set your API Key in `config.py` (register at http://api.football-data.org/).
3. Run tests: `pytest test_matches.py -s -v`

## Notes
- API Key is user-specific; replace it with your own for testing.
- Tests are validated with real API responses during development.

## Learning Notes
- See `Problem.json` for challenges encountered and solutions applied during development.