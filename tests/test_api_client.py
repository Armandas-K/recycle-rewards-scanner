import pytest
import requests
from unittest.mock import patch, MagicMock
from api.client import get_user, checkout

TEST_UID = "04:3a:78:9b:dd:2a:81"

# helper

def make_mock_response(json_data: dict) -> MagicMock:
    mock = MagicMock()
    mock.json.return_value = json_data
    mock.raise_for_status  = MagicMock()
    return mock

# get_user

def test_get_user_returns_correct_fields():
    data = {"found": True, "name": "Test User", "language": "en", "points": 100}
    with patch("api.client.requests.get", return_value=make_mock_response(data)):
        result = get_user(TEST_UID)
    assert result["found"] is True
    assert result["name"] == "Test User"
    assert result["language"] == "en"
    assert result["points"] == 100

def test_get_user_not_found():
    with patch("api.client.requests.get", return_value=make_mock_response({"found": False})):
        result = get_user(TEST_UID)
    assert result["found"] is False

def test_get_user_calls_correct_url():
    with patch("api.client.requests.get", return_value=make_mock_response({"found": False})) as mock_get:
        get_user(TEST_UID)
    url = mock_get.call_args[0][0]
    assert f"/api/v1/user/{TEST_UID}" in url

def test_get_user_request_exception_returns_defaults():
    with patch("api.client.requests.get", side_effect=requests.RequestException("error")):
        result = get_user(TEST_UID)
    assert result["found"] is False
    assert result["name"] == "User"
    assert result["language"] == "en"
    assert result["points"] == 0

def test_get_user_timeout_returns_defaults():
    with patch("api.client.requests.get", side_effect=requests.Timeout):
        result = get_user(TEST_UID)
    assert result["found"] is False

def test_get_user_does_not_raise():
    with patch("api.client.requests.get", side_effect=requests.RequestException("unexpected")):
        try:
            get_user(TEST_UID)
        except Exception:
            pytest.fail("get_user raised an exception instead of handling it")

# checkout

def test_checkout_success():
    with patch("api.client.requests.post", return_value=make_mock_response({"success": True})):
        result = checkout(TEST_UID, bottles=3, cans=2, points=21)
    assert result["success"] is True

def test_checkout_calls_correct_url():
    with patch("api.client.requests.post", return_value=make_mock_response({"success": True})) as mock_post:
        checkout(TEST_UID, bottles=1, cans=0, points=5)
    url = mock_post.call_args[0][0]
    assert "/api/v1/checkout" in url

def test_checkout_sends_user_uuid():
    with patch("api.client.requests.post", return_value=make_mock_response({"success": True})) as mock_post:
        checkout(TEST_UID, bottles=1, cans=0, points=5)
    assert mock_post.call_args[1]["json"]["user_uuid"] == TEST_UID

def test_checkout_sends_correct_bottle_and_can_count():
    with patch("api.client.requests.post", return_value=make_mock_response({"success": True})) as mock_post:
        checkout(TEST_UID, bottles=3, cans=2, points=21)
    payload = mock_post.call_args[1]["json"]
    assert payload["bottle_count"] == 3
    assert payload["can_count"] == 2

def test_checkout_sends_correct_points():
    with patch("api.client.requests.post", return_value=make_mock_response({"success": True})) as mock_post:
        checkout(TEST_UID, bottles=3, cans=2, points=21)
    assert mock_post.call_args[1]["json"]["points"] == 21

def test_checkout_sends_bin_id():
    with patch("api.client.requests.post", return_value=make_mock_response({"success": True})) as mock_post:
        checkout(TEST_UID, bottles=1, cans=0, points=5)
    assert "bin_id" in mock_post.call_args[1]["json"]

def test_checkout_zero_items_sends_zeros():
    with patch("api.client.requests.post", return_value=make_mock_response({"success": True})) as mock_post:
        checkout(TEST_UID, bottles=0, cans=0, points=0)
    payload = mock_post.call_args[1]["json"]
    assert payload["bottle_count"] == 0
    assert payload["can_count"] == 0
    assert payload["points"] == 0

def test_checkout_request_exception_returns_failure():
    with patch("api.client.requests.post", side_effect=requests.RequestException("error")):
        result = checkout(TEST_UID, bottles=1, cans=0, points=5)
    assert result["success"] is False

def test_checkout_timeout_returns_failure():
    with patch("api.client.requests.post", side_effect=requests.Timeout):
        result = checkout(TEST_UID, bottles=1, cans=0, points=5)
    assert result["success"] is False

def test_checkout_does_not_raise():
    with patch("api.client.requests.post", side_effect=requests.RequestException("unexpected")):
        try:
            checkout(TEST_UID, bottles=1, cans=0, points=5)
        except Exception:
            pytest.fail("checkout raised an exception instead of handling it")