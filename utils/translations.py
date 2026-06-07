import json
import os

_TRANSLATIONS: dict = {}

def _load() -> dict:
    path = os.path.join(os.path.dirname(__file__), "..", "data", "locales", "translations.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

_TRANSLATIONS = _load()

def get_text(language: str, screen: str, key: str) -> str:
    # fallback to english if language/key not found
    lang_data = _TRANSLATIONS.get(language) or _TRANSLATIONS.get("en", {})
    screen_data = lang_data.get(screen, {})
    if key not in screen_data:
        screen_data = _TRANSLATIONS.get("en", {}).get(screen, {})
    return screen_data.get(key, key)