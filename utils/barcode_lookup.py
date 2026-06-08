import urllib.request
import json
import pandas as pd
import os

from build_cache import CAN_SUFFIXES

BASE_URL = "https://world.openfoodfacts.org/api/v0/product"
CACHE_FILE = "data/cache/filtered_barcodes.csv"
TIMEOUT = 3

def _classify_tags(packaging_tags: str) -> str:
    if not isinstance(packaging_tags, str):
        return "bottle"
    tags = [t.strip() for t in packaging_tags.split(",")]
    if any(tag.endswith(suffix) for tag in tags for suffix in CAN_SUFFIXES):
        return "can"
    return "bottle"

def _load_cache() -> tuple[set, dict]:
    if not os.path.exists(CACHE_FILE):
        print("[LOOKUP] Cache file not found, run build_cache.py first")
        return set(), {}
    df = pd.read_csv(CACHE_FILE, usecols=["code", "packaging_tags"], dtype=str)
    df = df.dropna(subset=["code"])
    codes    = set(df["code"].str.strip())
    type_map = {
        row["code"].strip(): _classify_tags(row["packaging_tags"])
        for _, row in df.iterrows()
        if pd.notna(row["code"])
    }
    return codes, type_map

_CACHE, _TYPE_MAP = _load_cache()

def is_in_cache(barcode: str) -> bool:
    return barcode in _CACHE

def get_container_type(barcode: str) -> str:
    # returns "bottle" or "can
    # defaults to "bottle" for api only barcodes
    return _TYPE_MAP.get(barcode, "bottle")

def lookup(barcode: str) -> dict:
    # returns dict with keys:
    # found bool
    # name str
    # category str
    # flagged bool - true if not found with api, needs manual review

    url = f"{BASE_URL}/{barcode}.json"
    try:
        with urllib.request.urlopen(url, timeout=TIMEOUT) as response:
            data = json.loads(response.read())

        if data.get("status") == 1:
            product = data["product"]
            return {
                "found": True,
                "name": product.get("product_name", "Unknown"),
                "category": product.get("categories", "Unknown"),
                "flagged": False
            }

    except Exception as e:
        print(f"[LOOKUP] API error for {barcode}: {e}")

    return {
        "found": False,
        "name": "Unknown",
        "category": "Unknown",
        "flagged": True
    }