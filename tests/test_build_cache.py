import pytest
import pandas as pd
from unittest.mock import patch
from build_cache import is_accepted_container, build_cache

# is_accepted_container

def test_pet_bottle_accepted():
    assert is_accepted_container("en:pet-bottle") is True

def test_aluminium_can_accepted():
    assert is_accepted_container("en:aluminium") is True

def test_mixed_plastic_bottle_accepted():
    assert is_accepted_container("en:mixed-plastic-bottle") is True

def test_glass_bottle_rejected():
    assert is_accepted_container("en:glass-bottle") is False

def test_none_rejected():
    assert is_accepted_container(None) is False

def test_empty_string_rejected():
    assert is_accepted_container("") is False

def test_multiple_tags_one_valid():
    # row with mixed tags should pass if at least one matches
    assert is_accepted_container("en:cardboard,en:pet-bottle,en:sleeve") is True

def test_multiple_tags_none_valid():
    assert is_accepted_container("en:cardboard,en:glass-bottle") is False

# build_cache

def test_build_cache_filters_glass_bottle(sample_export_df, tmp_path):
    # glass bottle row should not appear in output
    output = tmp_path / "filtered.csv"
    with patch("build_cache.pd.read_csv", return_value=sample_export_df), \
         patch("build_cache.OUTPUT_PATH", str(output)):
        build_cache()

    result = pd.read_csv(output)
    assert "en:glass-bottle" not in result["packaging_tags"].values

def test_build_cache_keeps_valid_containers(sample_export_df, tmp_path):
    # valid container rows should all appear in output
    output = tmp_path / "filtered.csv"
    with patch("build_cache.pd.read_csv", return_value=sample_export_df), \
         patch("build_cache.OUTPUT_PATH", str(output)):
        build_cache()

    result = pd.read_csv(output, dtype=str)
    actual_codes = set(result["code"].dropna().values)
    expected_codes = {"5000193034559", "5054267007123", "5010251484851", "4056489010104"}

    assert expected_codes.issubset(actual_codes), \
        f"Missing from output: {expected_codes - actual_codes}"

def test_build_cache_output_has_correct_columns(sample_export_df, tmp_path):
    output = tmp_path / "filtered.csv"
    with patch("build_cache.pd.read_csv", return_value=sample_export_df), \
         patch("build_cache.OUTPUT_PATH", str(output)):
        build_cache()

    result = pd.read_csv(output)
    assert "code" in result.columns
    assert "product_name_en" in result.columns
    assert "packaging_tags" in result.columns
    assert "categories_tags" in result.columns

def test_build_cache_creates_output_file(sample_export_df, tmp_path):
    output = tmp_path / "filtered.csv"
    with patch("build_cache.pd.read_csv", return_value=sample_export_df), \
         patch("build_cache.OUTPUT_PATH", str(output)):
        build_cache()

    assert output.exists()