import json
import pytest
import pandas as pd
import urllib.error
from unittest.mock import patch, MagicMock
from utils.barcode_lookup import is_in_cache, lookup

# Barcodes

BARCODE_IN_CACHE  = "5449000125013"  # in filtered cache
BARCODE_API_ONLY  = "4335619173132"  # in API, not in cache
BARCODE_NOT_FOUND = "4062139030507"  # not in cache or API

TEST_CACHE = {BARCODE_IN_CACHE}

# Helpers

def make_api_response(found: bool, name: str = "", category: str = "") -> bytes:
    if found:
        return json.dumps({
            "status": 1,
            "product": {
                "product_name": name,
                "categories": category
            }
        }).encode()
    return json.dumps({"status": 0}).encode()

def mock_urlopen(response_bytes: bytes) -> MagicMock:
    mock = MagicMock()
    mock.__enter__ = lambda s: s
    mock.__exit__  = MagicMock(return_value=False)
    mock.read.return_value = response_bytes
    return mock

# is_in_cache

def test_in_cache_returns_true():
    with patch("utils.barcode_lookup._CACHE", TEST_CACHE):
        assert is_in_cache(BARCODE_IN_CACHE) is True

def test_not_in_cache_returns_false():
    with patch("utils.barcode_lookup._CACHE", TEST_CACHE):
        assert is_in_cache(BARCODE_API_ONLY) is False

def test_not_in_cache_or_api_returns_false():
    with patch("utils.barcode_lookup._CACHE", TEST_CACHE):
        assert is_in_cache(BARCODE_NOT_FOUND) is False

def test_empty_cache_always_returns_false():
    with patch("utils.barcode_lookup._CACHE", set()):
        assert is_in_cache(BARCODE_IN_CACHE) is False

# Cache Loading

def test_load_cache_reads_codes_correctly(tmp_path):
    # _load_cache should read codes from CSV into a set
    csv_file = tmp_path / "filtered_barcodes.csv"
    pd.DataFrame({"code": [BARCODE_IN_CACHE, BARCODE_API_ONLY]}).to_csv(csv_file, index=False)

    with patch("utils.barcode_lookup.CACHE_FILE", str(csv_file)):
        from utils.barcode_lookup import _load_cache
        cache = _load_cache()

    assert BARCODE_IN_CACHE in cache
    assert BARCODE_API_ONLY in cache

def test_load_cache_missing_file_returns_empty_set(tmp_path):
    with patch("utils.barcode_lookup.CACHE_FILE", str(tmp_path / "nonexistent.csv")):
        from utils.barcode_lookup import _load_cache
        cache = _load_cache()

    assert cache == set()

def test_load_cache_drops_null_codes(tmp_path):
    csv_file = tmp_path / "filtered_barcodes.csv"
    pd.DataFrame({"code": [BARCODE_IN_CACHE, None]}).to_csv(csv_file, index=False)

    with patch("utils.barcode_lookup.CACHE_FILE", str(csv_file)):
        from utils.barcode_lookup import _load_cache
        cache = _load_cache()

    assert None not in cache
    assert len(cache) == 1

# Lookup Found

def test_lookup_found_returns_correct_fields():
    response = make_api_response(
        found=True,
        name="Citrus Punch",
        category="en:beverages,en:artificially-sweetened-beverages"
    )
    with patch("urllib.request.urlopen", return_value=mock_urlopen(response)):
        result = lookup(BARCODE_IN_CACHE)

    assert result["found"] is True
    assert result["flagged"] is False
    assert result["name"] == "Citrus Punch"
    assert result["category"] == "en:beverages,en:artificially-sweetened-beverages"

def test_lookup_found_not_flagged():
    response = make_api_response(found=True, name="Citrus Punch")
    with patch("urllib.request.urlopen", return_value=mock_urlopen(response)):
        result = lookup(BARCODE_IN_CACHE)

    assert result["flagged"] is False

def test_lookup_missing_product_name_defaults_to_unknown():
    response = json.dumps({
        "status": 1,
        "product": {"categories": "en:beverages"}
    }).encode()
    mock = mock_urlopen(response)
    with patch("urllib.request.urlopen", return_value=mock):
        result = lookup(BARCODE_IN_CACHE)

    assert result["name"] == "Unknown"

# Lookup Not Found

def test_lookup_api_only_barcode_found():
    # barcode not in cache but in API should still return found
    response = make_api_response(found=True, name="Highland Glen")
    with patch("urllib.request.urlopen", return_value=mock_urlopen(response)):
        result = lookup(BARCODE_API_ONLY)

    assert result["found"] is True

def test_lookup_not_found_returns_flagged():
    response = make_api_response(found=False)
    with patch("urllib.request.urlopen", return_value=mock_urlopen(response)):
        result = lookup(BARCODE_NOT_FOUND)

    assert result["found"] is False
    assert result["flagged"] is True

def test_lookup_not_found_name_is_unknown():
    response = make_api_response(found=False)
    with patch("urllib.request.urlopen", return_value=mock_urlopen(response)):
        result = lookup(BARCODE_NOT_FOUND)

    assert result["name"] == "Unknown"
    assert result["category"] == "Unknown"

# Lookup API errors

def test_lookup_api_timeout_returns_flagged():
    with patch("urllib.request.urlopen", side_effect=TimeoutError("timed out")):
        result = lookup(BARCODE_IN_CACHE)

    assert result["found"] is False
    assert result["flagged"] is True

def test_lookup_api_error_does_not_raise():
    # API error should be handled and not crash the program
    with patch("urllib.request.urlopen", side_effect=Exception("unexpected")):
        try:
            result = lookup(BARCODE_IN_CACHE)
        except Exception:
            pytest.fail("lookup() raised an exception instead of handling it")

def test_lookup_returns_all_expected_keys_on_error():
    with patch("urllib.request.urlopen", side_effect=Exception("error")):
        result = lookup(BARCODE_IN_CACHE)

    assert "found" in result
    assert "name" in result
    assert "category" in result
    assert "flagged" in result