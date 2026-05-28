import urllib.request
import json
import pandas as pd
import os

BASE_URL = "https://world.openfoodfacts.org/api/v0/product"
CACHE_FILE = "cache/filtered_barcodes.csv"
TIMEOUT = 3

def _load_cache() -> set:
    if not os.path.exists(CACHE_FILE):
        print("[LOOKUP] Cache file not found, run build_cache.py first")
        return set()
    df = pd.read_csv(CACHE_FILE, usecols=["code"], dtype=str)
    return set(df["code"].dropna().str.strip())

_CACHE: set = _load_cache()

def is_in_cache(barcode: str) -> bool:
    return barcode in _CACHE

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
                "found":    True,
                "name":     product.get("product_name", "Unknown"),
                "category": product.get("categories", "Unknown"),
                "flagged":  False
            }

    except Exception as e:
        print(f"[LOOKUP] API error for {barcode}: {e}")

    # valid barcode structure but not in Open Food Facts
    return {
        "found":    False,
        "name":     "Unknown",
        "category": "Unknown",
        "flagged":  True
    }