import pytest
from utils.translations import get_text

LANGUAGES = ["en", "ur", "pa", "bn", "pl"]

EXPECTED_KEYS = {
    "welcome": ["greeting", "subtitle"],
    "scanning": ["heading", "bottles", "cans", "points"],
    "loading": ["heading", "subtitle"],
}

# all languages have all keys

@pytest.mark.parametrize("language", LANGUAGES)
@pytest.mark.parametrize("screen,keys", EXPECTED_KEYS.items())
def test_all_keys_present_for_language(language, screen, keys):
    for key in keys:
        result = get_text(language, screen, key)
        assert isinstance(result, str), f"Expected string for {language}/{screen}/{key}"
        assert len(result) > 0, f"Empty translation for {language}/{screen}/{key}"

# english values

def test_english_bottles_label():
    assert get_text("en", "scanning", "bottles") == "bottles"

def test_english_cans_label():
    assert get_text("en", "scanning", "cans") == "cans"

def test_english_loading_heading():
    assert get_text("en", "loading", "heading") == "Processing"

def test_english_loading_subtitle():
    assert get_text("en", "loading", "subtitle") == "Please wait"

# greeting name placeholder

@pytest.mark.parametrize("language", LANGUAGES)
def test_greeting_contains_name_placeholder(language):
    greeting = get_text(language, "welcome", "greeting")
    assert "{name}" in greeting, f"Missing {{name}} placeholder in {language} greeting"

@pytest.mark.parametrize("language", LANGUAGES)
def test_greeting_formats_name_correctly(language):
    greeting = get_text(language, "welcome", "greeting")
    formatted = greeting.format(name="Alice")
    assert "Alice" in formatted

# fallback behaviour

def test_unknown_language_falls_back_to_english():
    result = get_text("xx", "scanning", "bottles")
    assert result == get_text("en", "scanning", "bottles")

def test_unknown_key_returns_key_string():
    result = get_text("en", "scanning", "nonexistent_key")
    assert result == "nonexistent_key"

def test_unknown_screen_returns_key_string():
    result = get_text("en", "nonexistent_screen", "bottles")
    assert result == "bottles"

def test_unknown_language_and_key_returns_key_string():
    result = get_text("xx", "scanning", "nonexistent_key")
    assert result == "nonexistent_key"

# languages are distinct from english

@pytest.mark.parametrize("language", ["ur", "pa", "bn", "pl"])
def test_non_english_bottles_differs_from_english(language):
    # confirms each language has its own translation, not just English
    english = get_text("en", "scanning", "bottles")
    other = get_text(language, "scanning", "bottles")
    assert other != english, f"{language} bottles label matches english, missing translation"

@pytest.mark.parametrize("language", ["ur", "pa", "bn", "pl"])
def test_non_english_loading_heading_differs_from_english(language):
    english = get_text("en", "loading", "heading")
    other = get_text(language, "loading", "heading")
    assert other != english, f"{language} loading heading matches english, missing translation"